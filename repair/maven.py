"""Run the benchmark's JUnit tests through Maven and read the Surefire reports."""
import json
import os
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCHMARK = ROOT / "benchmark"
BUGS = ROOT / "bugs"
MAIN = Path("src/main/java/bench")
TESTS = BENCHMARK / "src/test/java/bench"


def load_bugs():
    return json.loads((BUGS / "bugs.json").read_text(encoding="utf-8"))


def buggy_source(bug):
    return (BUGS / bug["id"] / f"{bug['class']}.java").read_text(encoding="utf-8")


def reference_source(bug):
    return (BENCHMARK / MAIN / f"{bug['class']}.java").read_text(encoding="utf-8")


def visible_test_source(bug):
    return (TESTS / f"{bug['class']}VisibleTest.java").read_text(encoding="utf-8")


def mvn_executable():
    exe = os.environ.get("MVN") or shutil.which("mvn") or shutil.which("mvn.cmd")
    if not exe:
        raise RuntimeError("Maven not found: install Maven 3.9+ and put it on PATH, or set MVN")
    return exe


def make_workspace(dest):
    """Copy the benchmark project to `dest` so patches never touch the reference sources."""
    shutil.copytree(BENCHMARK, dest, ignore=shutil.ignore_patterns("target"))
    return Path(dest)


def parse_report(path):
    """Summarise a JUnit XML report (Surefire or pytest format)."""
    root = ET.parse(path).getroot()
    cases, failures = [], []
    for case in root.iter("testcase"):
        status = "passed"
        for tag in ("failure", "error"):
            el = case.find(tag)
            if el is not None:
                status = tag
                failures.append({
                    "test": case.get("name"),
                    "type": el.get("type", ""),
                    "message": el.get("message") or "",
                    "trace": el.text or "",
                })
        if case.find("skipped") is not None:
            status = "skipped"
        cases.append({"class": case.get("classname", ""), "name": case.get("name"), "status": status})
    return {"tests": len(cases), "failed": len(failures), "failures": failures, "cases": cases}


def compile_errors(output, workspace=None):
    """Keep only the compiler error lines, with the temporary workspace path removed."""
    lines = [ln for ln in output.splitlines() if ln.startswith("[ERROR]") and (".java" in ln or "symbol" in ln)]
    text = "\n".join(lines[:20])
    if workspace:
        for prefix in {str(workspace), str(Path(workspace))}:
            text = text.replace(prefix + "/", "").replace(prefix + "\\", "").replace(prefix, "")
    return text


def run_tests(workspace, cls, timeout=300):
    """Compile the workspace and run the visible and hidden tests of one class."""
    names = {"visible": f"{cls}VisibleTest", "hidden": f"{cls}HiddenTest"}
    reports = Path(workspace) / "target" / "surefire-reports"
    shutil.rmtree(reports, ignore_errors=True)
    cmd = [mvn_executable(), "-B", "test", "-Dtest=" + ",".join(names.values()),
           "-Dsurefire.failIfNoSpecifiedTests=false", "-Dmaven.test.failure.ignore=true"]
    if os.environ.get("MVN_OFFLINE"):
        cmd.insert(1, "-o")
    result = {"compiled": True, "timeout": False, "compile_errors": "", "visible": None, "hidden": None}
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, timeout=timeout)
        output = proc.stdout + proc.stderr
        if proc.returncode != 0:
            if "COMPILATION ERROR" in output:
                result["compiled"] = False
                result["compile_errors"] = compile_errors(output, workspace)
            elif "There was a timeout" in output:
                result["timeout"] = True
            else:
                raise RuntimeError("Maven failed for a reason other than compilation:\n" + output[-3000:])
    except subprocess.TimeoutExpired:
        result["timeout"] = True
    result["seconds"] = round(time.monotonic() - start, 2)
    if result["compiled"]:
        for kind, name in names.items():
            path = reports / f"TEST-bench.{name}.xml"
            # a missing report after a fork timeout counts as one failed test
            result[kind] = parse_report(path) if path.exists() else {"tests": 1, "failed": 1, "failures": [], "cases": []}
    return result


def passed(result, kind):
    report = result.get(kind)
    return bool(result.get("compiled") and report and report["tests"] > 0 and report["failed"] == 0)


def _trim_trace(trace, max_frames=8):
    lines = [ln.rstrip() for ln in trace.strip().splitlines()]
    if not lines:
        return ""
    frames = [ln for ln in lines[1:] if ln.strip().startswith("at bench.") or ln.strip().startswith("Caused by")]
    return "\n".join([lines[0]] + frames[:max_frames])


def diagnostics(result):
    """Execution diagnostics for the visible tests: compiler errors or failure messages plus stack traces."""
    if not result.get("compiled"):
        return "Compilation failed:\n" + (result.get("compile_errors") or "(no compiler output)")
    if result.get("timeout"):
        return "The test run timed out (possible infinite loop)."
    report = result.get("visible") or {}
    parts = [f"Tests run: {report.get('tests', 0)}, Failures: {report.get('failed', 0)}"]
    for f in report.get("failures", []):
        parts.append(f"{f['test']} FAILED\n{_trim_trace(f['trace']) or f['type'] + ': ' + f['message']}")
    return "\n\n".join(parts)
