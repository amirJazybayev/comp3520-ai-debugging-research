import pytest

from repair.analyze import markdown, mcnemar_exact, paired, sessions, summarize


def attempt(bug, cond, n, visible, hidden, repeat=1, compiled=True):
    return {"run_id": "R", "model": "m", "bug": bug, "category": "cat", "condition": cond, "repeat": repeat,
            "attempt": n, "compiled": compiled, "visible_pass": visible, "hidden_pass": hidden,
            "changed_lines": 2, "prompt_tokens": 10, "completion_tokens": 5, "llm_seconds": 1.0}


RECORDS = [
    # b01: baseline fixes on attempt 2, diagnostics on attempt 1
    attempt("b01", "baseline", 1, False, False, compiled=False), attempt("b01", "baseline", 2, True, True),
    attempt("b01", "diagnostics", 1, True, True),
    # b02: baseline overfits (visible passes, hidden fails); diagnostics correct
    attempt("b02", "baseline", 1, True, False), attempt("b02", "diagnostics", 1, True, True),
    # b03: both fail after 2 attempts
    attempt("b03", "baseline", 1, False, False), attempt("b03", "baseline", 2, False, False),
    attempt("b03", "diagnostics", 1, False, False), attempt("b03", "diagnostics", 2, False, False),
]


def test_sessions_collapse_attempts():
    rows = {(r["bug"], r["condition"]): r for r in sessions(RECORDS)}
    assert len(rows) == 6
    b01 = rows[("b01", "baseline")]
    assert b01["attempts"] == 2 and b01["correct"] and not b01["first_compiled"] and not b01["first_attempt_correct"]
    assert b01["tokens"] == 30
    assert rows[("b02", "baseline")]["plausible"] and not rows[("b02", "baseline")]["correct"]


def test_summarize_metrics():
    s = summarize(sessions(RECORDS))
    base, diag = s["baseline"], s["diagnostics"]
    assert base["sessions"] == 3 and base["attempts"] == 5
    assert base["compile_rate"] == pytest.approx(4 / 5)
    assert base["plausible"] == 2 and base["correct"] == 1 and base["overfitting"] == 1
    assert base["mean_attempts_plausible"] == pytest.approx(1.5)
    assert diag["correct"] == 2 and diag["first_attempt_correct"] == 2 and diag["overfitting"] == 0


def test_mcnemar_exact_known_values():
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(0, 5) == pytest.approx(0.0625)
    assert mcnemar_exact(3, 3) == 1.0
    assert mcnemar_exact(1, 9) == pytest.approx(2 * (1 + 10) / 1024)


def test_paired_counts_discordant_sessions():
    p = paired(sessions(RECORDS))
    assert p["both"] == 1 and p["neither"] == 1 and p["only_diagnostics"] == 1 and p["only_baseline"] == 0


def test_markdown_contains_tables():
    md = markdown(sessions(RECORDS))
    assert "| Correct repair (visible + hidden pass) | 1/3 (33%) | 2/3 (67%) |" in md
    assert "McNemar" in md and "| b02 | cat | 0/1 | 1/1 |" in md
