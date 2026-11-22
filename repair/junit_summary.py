"""Render JUnit XML reports as a Markdown table for the GitHub Actions job summary.

  python -m repair.junit_summary "Title" report1.xml report2.xml ... >> $GITHUB_STEP_SUMMARY
"""
import sys

from .maven import parse_report

ICON = {"passed": "✅", "failure": "❌", "error": "💥", "skipped": "⏭️"}


def render(title, paths):
    cases = [c for p in paths for c in parse_report(p)["cases"]]
    bad = sum(c["status"] in ("failure", "error") for c in cases)
    lines = [f"## {title}", "", f"**{len(cases) - bad}/{len(cases)} passed**", "",
             "| | Test class | Test |", "|---|---|---|"]
    lines += [f"| {ICON.get(c['status'], '?')} | {c['class']} | {c['name']} |" for c in cases]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(render(sys.argv[1], sys.argv[2:]))
