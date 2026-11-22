"""Aggregate raw attempt logs into the tables used in the report.

  python -m repair.analyze                      # all results/runs/*/attempts.jsonl
  python -m repair.analyze results/runs/X/attempts.jsonl
Writes results/summary.md and results/sessions.csv.
"""
import csv
import json
import sys
from collections import defaultdict
from math import comb
from pathlib import Path


def load(paths):
    records = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            records += [json.loads(line) for line in fh if line.strip()]
    return records


def sessions(records):
    """Collapse attempts into one row per (run, bug, condition, repeat) session."""
    groups = defaultdict(list)
    for r in records:
        groups[(r["run_id"], r["bug"], r["condition"], r["repeat"])].append(r)
    rows = []
    for (run_id, bug, condition, repeat), attempts in sorted(groups.items()):
        attempts.sort(key=lambda r: r["attempt"])
        final = attempts[-1]
        rows.append({
            "run_id": run_id, "model": final.get("model"), "bug": bug, "category": final["category"],
            "condition": condition, "repeat": repeat, "attempts": len(attempts),
            "first_compiled": attempts[0]["compiled"],
            "compiled_attempts": sum(a["compiled"] for a in attempts),
            "plausible": final["visible_pass"],
            "correct": final["visible_pass"] and final["hidden_pass"],
            "first_attempt_correct": attempts[0]["visible_pass"] and attempts[0]["hidden_pass"],
            "changed_lines": final["changed_lines"],
            "tokens": sum((a.get("prompt_tokens") or 0) + (a.get("completion_tokens") or 0) for a in attempts),
            "llm_seconds": round(sum(a.get("llm_seconds") or 0 for a in attempts), 2),
        })
    return rows


def _pct(k, n):
    return f"{k}/{n} ({100 * k / n:.0f}%)" if n else "0/0"


def summarize(rows):
    out = {}
    for cond in sorted({r["condition"] for r in rows}):
        s = [r for r in rows if r["condition"] == cond]
        n = len(s)
        attempts = sum(r["attempts"] for r in s)
        plausible = [r for r in s if r["plausible"]]
        out[cond] = {
            "sessions": n,
            "attempts": attempts,
            "compile_rate": sum(r["compiled_attempts"] for r in s) / attempts if attempts else 0,
            "first_attempt_compiled": sum(r["first_compiled"] for r in s),
            "plausible": len(plausible),
            "correct": sum(r["correct"] for r in s),
            "first_attempt_correct": sum(r["first_attempt_correct"] for r in s),
            "overfitting": sum(r["plausible"] and not r["correct"] for r in s),
            "mean_attempts_plausible": sum(r["attempts"] for r in plausible) / len(plausible) if plausible else None,
            "mean_tokens": sum(r["tokens"] for r in s) / n if n else 0,
            "mean_llm_seconds": sum(r["llm_seconds"] for r in s) / n if n else 0,
        }
    return out


def mcnemar_exact(b, c):
    """Two-sided exact McNemar test: b, c are the discordant pair counts."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(comb(n, i) for i in range(0, min(b, c) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def paired(rows, a="baseline", b="diagnostics", key="correct"):
    """Pair sessions of the same bug/repeat/run and count discordant outcomes."""
    by = {(r["run_id"], r["bug"], r["repeat"], r["condition"]): r[key] for r in rows}
    only_a = only_b = both = neither = 0
    for (run_id, bug, repeat, cond), val in by.items():
        if cond != a or (run_id, bug, repeat, b) not in by:
            continue
        other = by[(run_id, bug, repeat, b)]
        both += val and other
        neither += not val and not other
        only_a += val and not other
        only_b += other and not val
    return {"both": both, "neither": neither, f"only_{a}": only_a, f"only_{b}": only_b,
            "p_value": mcnemar_exact(only_a, only_b)}


def markdown(rows):
    summary = summarize(rows)
    conds = list(summary)
    lines = ["# Results summary", "", f"Models: {', '.join(sorted({str(r['model']) for r in rows}))}", "",
             "| Metric | " + " | ".join(conds) + " |", "|---|" + "---|" * len(conds)]

    def row(label, fn):
        lines.append(f"| {label} | " + " | ".join(fn(summary[c]) for c in conds) + " |")

    row("Sessions", lambda s: str(s["sessions"]))
    row("Total attempts", lambda s: str(s["attempts"]))
    row("Compilation rate (all attempts)", lambda s: f"{100 * s['compile_rate']:.0f}%")
    row("First attempt compiles", lambda s: _pct(s["first_attempt_compiled"], s["sessions"]))
    row("Plausible repair (visible test passes)", lambda s: _pct(s["plausible"], s["sessions"]))
    row("Correct repair (visible + hidden pass)", lambda s: _pct(s["correct"], s["sessions"]))
    row("Correct on first attempt", lambda s: _pct(s["first_attempt_correct"], s["sessions"]))
    row("Overfitting (plausible but hidden fails)", lambda s: _pct(s["overfitting"], s["plausible"]))
    row("Mean attempts per plausible repair",
        lambda s: f"{s['mean_attempts_plausible']:.2f}" if s["mean_attempts_plausible"] else "-")
    row("Mean tokens per session", lambda s: f"{s['mean_tokens']:.0f}")
    row("Mean LLM time per session (s)", lambda s: f"{s['mean_llm_seconds']:.1f}")
    if {"baseline", "diagnostics"} <= set(conds):
        p = paired(rows)
        lines += ["", "## Paired comparison (correct repairs, exact McNemar test)", "",
                  f"Both correct: {p['both']}, neither: {p['neither']}, only baseline: {p['only_baseline']}, "
                  f"only diagnostics: {p['only_diagnostics']}, p = {p['p_value']:.4f}"]
    lines += ["", "## Correct repairs per bug", "", "| Bug | Category | " + " | ".join(conds) + " |",
              "|---|---|" + "---|" * len(conds)]
    for bug in sorted({r["bug"] for r in rows}):
        rs = [r for r in rows if r["bug"] == bug]
        cells = []
        for c in conds:
            cs = [r for r in rs if r["condition"] == c]
            cells.append(f"{sum(r['correct'] for r in cs)}/{len(cs)}")
        lines.append(f"| {bug} | {rs[0]['category']} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    paths = argv or sorted(str(p) for p in Path("results/runs").glob("*/attempts.jsonl"))
    if not paths:
        print("no attempts.jsonl files found")
        return 1
    rows = sessions(load(paths))
    Path("results").mkdir(exist_ok=True)
    with open("results/sessions.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    review = Path("results/manual_review.csv")
    if not review.exists():  # never overwrite labels a human has already entered
        with review.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["bug", "condition", "repeat", "patch", "hidden_pass",
                        "reviewer1_correct(Y/N)", "reviewer2_correct(Y/N)", "notes"])
            for r in rows:
                if r["plausible"]:
                    patch = f"results/runs/{r['run_id']}/patches/{r['bug']}_{r['condition']}_r{r['repeat']}_a{r['attempts']}.java"
                    w.writerow([r["bug"], r["condition"], r["repeat"], patch, r["correct"], "", "", ""])
    md = markdown(rows)
    Path("results/summary.md").write_text(md, encoding="utf-8")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
