"""Run the repair experiment, or validate the benchmark.

  python -m repair.experiment validate
  python -m repair.experiment run --repeats 3 --max-attempts 3
"""
import argparse
import difflib
import json
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from . import maven
from .prompts import CONDITIONS, SYSTEM, extract_java, initial_prompt, retry_prompt


def changed_lines(a, b):
    """Number of added + removed lines between two sources (patch size)."""
    diff = difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
    return sum(1 for ln in diff if ln[:1] in "+-" and not ln.startswith(("+++", "---")))


def run_session(bug, condition, llm, evaluate, max_attempts):
    """One repair session: up to `max_attempts` LLM patches, stopping when the visible test passes.

    `evaluate(source)` compiles `source` in place of the buggy class and returns a maven.run_tests result.
    Returns one record per attempt; the reply text and patch are included for archiving.
    """
    cls = bug["class"]
    buggy = maven.buggy_source(bug)
    first = evaluate(buggy)
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": initial_prompt(cls, buggy, maven.visible_test_source(bug), condition,
                                                   maven.diagnostics(first))},
    ]
    records = []
    for attempt in range(1, max_attempts + 1):
        reply = llm(messages)
        patch = extract_java(reply["text"], cls)
        if patch is None:
            result = {"compiled": False, "timeout": False, "no_code": True, "visible": None, "hidden": None, "seconds": 0,
                      "compile_errors": f"No ```java code block declaring class {cls} was found in the reply."}
        else:
            result = evaluate(patch)
        rec = {
            "bug": bug["id"], "class": cls, "category": bug["category"], "condition": condition, "attempt": attempt,
            "compiled": result["compiled"], "no_code": result.get("no_code", False), "timeout": result.get("timeout", False),
            "visible_pass": maven.passed(result, "visible"), "hidden_pass": maven.passed(result, "hidden"),
            "visible_failed": (result.get("visible") or {}).get("failed"),
            "hidden_failed": (result.get("hidden") or {}).get("failed"),
            "hidden_tests": (result.get("hidden") or {}).get("tests"),
            "changed_lines": changed_lines(buggy, patch) if patch else None,
            "prompt_tokens": reply.get("prompt_tokens"), "completion_tokens": reply.get("completion_tokens"),
            "llm_seconds": reply.get("seconds"), "test_seconds": result.get("seconds"),
            "reply": reply["text"], "patch": patch,
        }
        records.append(rec)
        if rec["visible_pass"]:
            break
        messages += [{"role": "assistant", "content": reply["text"]},
                     {"role": "user", "content": retry_prompt(cls, condition, result["compiled"], maven.diagnostics(result))}]
    records[-1]["final"] = True
    return records


def _workspace_evaluator(workspace, cls):
    target = workspace / maven.MAIN / f"{cls}.java"
    reference = target.read_text(encoding="utf-8")

    def evaluate(source):
        target.write_text(source, encoding="utf-8")
        return maven.run_tests(workspace, cls)

    evaluate.restore = lambda: target.write_text(reference, encoding="utf-8")
    return evaluate


def cmd_validate(_args):
    """Each buggy version must compile and fail at least one visible test; references must pass everything."""
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        ws = maven.make_workspace(Path(tmp) / "ws")
        for bug in maven.load_bugs():
            evaluate = _workspace_evaluator(ws, bug["class"])
            buggy = evaluate(maven.buggy_source(bug))
            ref = evaluate(maven.reference_source(bug))
            good = buggy["compiled"] and not maven.passed(buggy, "visible") \
                and maven.passed(ref, "visible") and maven.passed(ref, "hidden")
            ok &= good
            print(f"{bug['id']} {bug['class']:<22} buggy fails visible: {not maven.passed(buggy, 'visible')!s:<5} "
                  f"reference passes visible+hidden: {maven.passed(ref, 'visible') and maven.passed(ref, 'hidden')!s:<5} "
                  f"{'OK' if good else 'INVALID'}")
    print("benchmark valid" if ok else "benchmark INVALID")
    return 0 if ok else 1


def cmd_run(args):
    from .llm import ChatClient
    llm = ChatClient(temperature=args.temperature)
    bugs = [b for b in maven.load_bugs() if not args.bugs or b["id"] in args.bugs.split(",")]
    conditions = args.conditions.split(",")
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "config.json").write_text(json.dumps({
        "run_id": run_id, "model": llm.model, "base_url": llm.base_url, "temperature": args.temperature,
        "reasoning_effort": llm.reasoning_effort or None, "timeout_seconds": llm.timeout,
        "repeats": args.repeats, "max_attempts": args.max_attempts, "bugs": [b["id"] for b in bugs],
        "conditions": conditions, "started": datetime.now(timezone.utc).isoformat()}, indent=2))
    log = out_dir / "attempts.jsonl"
    with tempfile.TemporaryDirectory() as tmp:
        ws = maven.make_workspace(Path(tmp) / "ws")
        # interleave conditions per bug so drift in the model/API affects both equally
        for repeat in range(1, args.repeats + 1):
            for bug in bugs:
                for condition in conditions:
                    started = time.monotonic()
                    evaluate = _workspace_evaluator(ws, bug["class"])
                    records = run_session(bug, condition, llm, evaluate, args.max_attempts)
                    evaluate.restore()  # a broken patch must not leak into the next session's build
                    with log.open("a", encoding="utf-8") as fh:
                        for rec in records:
                            stem = f"{bug['id']}_{condition}_r{repeat}_a{rec['attempt']}"
                            (out_dir / "replies").mkdir(exist_ok=True)
                            (out_dir / "replies" / f"{stem}.md").write_text(rec.pop("reply"), encoding="utf-8")
                            patch = rec.pop("patch")
                            if patch:
                                (out_dir / "patches").mkdir(exist_ok=True)
                                (out_dir / "patches" / f"{stem}.java").write_text(patch, encoding="utf-8")
                            rec.update(run_id=run_id, model=llm.model, repeat=repeat)
                            fh.write(json.dumps(rec) + "\n")
                    final = records[-1]
                    print(f"r{repeat} {bug['id']} {condition:<11} attempts={len(records)} "
                          f"visible={final['visible_pass']} hidden={final['hidden_pass']} "
                          f"({time.monotonic() - started:.0f}s)", flush=True)
    print(f"raw results: {log}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m repair.experiment")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate", help="check that every buggy version fails and every reference passes")
    r = sub.add_parser("run", help="run the repair experiment against the configured LLM")
    r.add_argument("--bugs", default="", help="comma-separated bug ids (default: all)")
    r.add_argument("--conditions", default=",".join(CONDITIONS))
    r.add_argument("--repeats", type=int, default=3)
    r.add_argument("--max-attempts", type=int, default=3)
    r.add_argument("--temperature", type=float, default=0.2)
    r.add_argument("--out", default="results/runs")
    r.add_argument("--run-id", default="")
    args = p.parse_args(argv)
    return cmd_validate(args) if args.cmd == "validate" else cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
