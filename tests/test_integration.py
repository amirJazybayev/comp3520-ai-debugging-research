"""End-to-end checks with the real Maven build (run in CI's benchmark job)."""
import shutil

import pytest

from repair import maven
from repair.experiment import _workspace_evaluator, run_session

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not (shutil.which("mvn") or shutil.which("mvn.cmd")), reason="Maven not installed"),
]


class ReplayLLM:
    """Stands in for the model by returning a fixed source file."""

    def __init__(self, source):
        self.source = source

    def __call__(self, messages):
        return {"text": f"```java\n{self.source}```", "prompt_tokens": 0, "completion_tokens": 0, "seconds": 0}


@pytest.fixture(scope="module")
def workspace(tmp_path_factory):
    return maven.make_workspace(tmp_path_factory.mktemp("bench") / "ws")


def bug(bug_id):
    return next(b for b in maven.load_bugs() if b["id"] == bug_id)


def test_reference_patch_is_a_correct_repair(workspace):
    b = bug("b04")
    evaluate = _workspace_evaluator(workspace, b["class"])
    recs = run_session(b, "diagnostics", ReplayLLM(maven.reference_source(b)), evaluate, max_attempts=3)
    evaluate.restore()
    assert len(recs) == 1 and recs[0]["visible_pass"] and recs[0]["hidden_pass"]


def test_unchanged_buggy_code_is_never_plausible(workspace):
    b = bug("b04")
    evaluate = _workspace_evaluator(workspace, b["class"])
    recs = run_session(b, "baseline", ReplayLLM(maven.buggy_source(b)), evaluate, max_attempts=2)
    evaluate.restore()
    assert len(recs) == 2 and not recs[-1]["visible_pass"]


def test_non_compiling_patch_is_detected(workspace):
    b = bug("b01")
    evaluate = _workspace_evaluator(workspace, b["class"])
    broken = maven.reference_source(b).replace("long gross", "lng gross")
    recs = run_session(b, "diagnostics", ReplayLLM(broken), evaluate, max_attempts=1)
    evaluate.restore()
    assert not recs[0]["compiled"]


def test_overfitting_patch_passes_visible_but_not_hidden(workspace):
    b = bug("b02")
    evaluate = _workspace_evaluator(workspace, b["class"])
    naive = maven.buggy_source(b).replace("return totalItems / pageSize;", "return (totalItems + pageSize - 1) / pageSize;")
    recs = run_session(b, "baseline", ReplayLLM(naive), evaluate, max_attempts=1)
    evaluate.restore()
    assert recs[0]["visible_pass"] and not recs[0]["hidden_pass"]


def test_stack_trace_reaches_diagnostics(workspace):
    b = bug("b04")
    evaluate = _workspace_evaluator(workspace, b["class"])
    result = evaluate(maven.buggy_source(b))
    evaluate.restore()
    d = maven.diagnostics(result)
    assert "ArrayIndexOutOfBoundsException" in d and "at bench.RingBuffer.add" in d
