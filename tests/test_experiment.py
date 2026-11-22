from repair import maven
from repair.experiment import changed_lines, run_session

BUG = next(b for b in maven.load_bugs() if b["id"] == "b01")
FIXED = maven.reference_source(BUG)
BUGGY = maven.buggy_source(BUG)
VISIBLE_FAIL = {"compiled": True, "seconds": 1,
                "visible": {"tests": 1, "failed": 1, "failures": [{"test": "t", "type": "AssertionFailedError",
                                                                   "message": "expected: <900> but was: <1000>",
                                                                   "trace": "AssertionFailedError: expected: <900> but was: <1000>"}]},
                "hidden": {"tests": 5, "failed": 2, "failures": []}}
ALL_PASS = {"compiled": True, "seconds": 1, "visible": {"tests": 1, "failed": 0, "failures": []},
            "hidden": {"tests": 5, "failed": 0, "failures": []}}


class FakeLLM:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []

    def __call__(self, messages):
        self.calls.append([dict(m) for m in messages])
        return {"text": self.replies.pop(0), "prompt_tokens": 100, "completion_tokens": 50, "seconds": 0.1}


def fake_evaluate(source):
    return ALL_PASS if "quantity >= 10" in source else VISIBLE_FAIL


def block(src):
    return f"```java\n{src}```"


def test_stops_at_first_attempt_that_passes_visible_test():
    llm = FakeLLM([block(BUGGY), block(FIXED), block(FIXED)])
    recs = run_session(BUG, "baseline", llm, fake_evaluate, max_attempts=3)
    assert [r["attempt"] for r in recs] == [1, 2]
    assert recs[-1]["final"] and recs[-1]["visible_pass"] and recs[-1]["hidden_pass"]
    assert recs[-1]["changed_lines"] == 2
    assert len(llm.calls) == 2


def test_gives_up_after_max_attempts():
    recs = run_session(BUG, "diagnostics", FakeLLM([block(BUGGY)] * 3), fake_evaluate, max_attempts=3)
    assert len(recs) == 3 and not recs[-1]["visible_pass"] and recs[-1]["final"]


def test_reply_without_code_counts_as_not_compiled():
    recs = run_session(BUG, "baseline", FakeLLM(["I think the bug is on line 20."]), fake_evaluate, max_attempts=1)
    assert recs[0]["no_code"] and not recs[0]["compiled"] and recs[0]["changed_lines"] is None


def test_only_diagnostics_condition_sees_execution_output():
    for cond, expect in (("baseline", False), ("diagnostics", True)):
        llm = FakeLLM([block(BUGGY), block(FIXED)])
        run_session(BUG, cond, llm, fake_evaluate, max_attempts=2)
        first, retry = llm.calls[0][1]["content"], llm.calls[1][-1]["content"]
        assert ("but was: <1000>" in first) is expect
        assert ("but was: <1000>" in retry) is expect


def test_hidden_test_source_is_never_sent():
    llm = FakeLLM([block(BUGGY), block(BUGGY)])
    run_session(BUG, "diagnostics", llm, fake_evaluate, max_attempts=2)
    sent = " ".join(m["content"] for call in llm.calls for m in call)
    assert "BulkPricingHiddenTest" not in sent and "belowThresholdHasNoDiscount" not in sent


def test_changed_lines():
    assert changed_lines("a\nb\nc", "a\nB\nc") == 2
    assert changed_lines("a", "a") == 0
