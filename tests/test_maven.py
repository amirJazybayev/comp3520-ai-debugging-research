from repair import maven

SUREFIRE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="bench.FooVisibleTest" tests="3" failures="1" errors="1">
  <testcase name="ok" classname="bench.FooVisibleTest" time="0.01"/>
  <testcase name="wrongValue" classname="bench.FooVisibleTest" time="0.01">
    <failure message="expected: &lt;3&gt; but was: &lt;2&gt;" type="org.opentest4j.AssertionFailedError">org.opentest4j.AssertionFailedError: expected: &lt;3&gt; but was: &lt;2&gt;
	at org.junit.jupiter.api.AssertionUtils.fail(AssertionUtils.java:151)
	at bench.FooVisibleTest.wrongValue(FooVisibleTest.java:10)
	at java.base/java.lang.reflect.Method.invoke(Method.java:580)
</failure>
  </testcase>
  <testcase name="crash" classname="bench.FooVisibleTest" time="0.01">
    <error message="Index 3 out of bounds for length 3" type="java.lang.ArrayIndexOutOfBoundsException">java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
	at bench.Foo.add(Foo.java:27)
	at bench.FooVisibleTest.crash(FooVisibleTest.java:15)
</error>
  </testcase>
</testsuite>
"""


def write(tmp_path, text=SUREFIRE_XML):
    p = tmp_path / "TEST-bench.FooVisibleTest.xml"
    p.write_text(text, encoding="utf-8")
    return p


def test_parse_report_counts_failures_and_errors(tmp_path):
    r = maven.parse_report(write(tmp_path))
    assert r["tests"] == 3 and r["failed"] == 2
    assert [c["status"] for c in r["cases"]] == ["passed", "failure", "error"]
    assert r["failures"][1]["type"] == "java.lang.ArrayIndexOutOfBoundsException"


def test_parse_report_handles_testsuites_root(tmp_path):
    xml = '<testsuites><testsuite name="x"><testcase classname="t" name="a"/></testsuite></testsuites>'
    r = maven.parse_report(write(tmp_path, xml))
    assert r["tests"] == 1 and r["failed"] == 0


def test_passed_requires_compilation_and_no_failures():
    ok = {"compiled": True, "visible": {"tests": 2, "failed": 0}}
    assert maven.passed(ok, "visible")
    assert not maven.passed({"compiled": True, "visible": {"tests": 2, "failed": 1}}, "visible")
    assert not maven.passed({"compiled": True, "visible": {"tests": 0, "failed": 0}}, "visible")
    assert not maven.passed({"compiled": False, "visible": None}, "visible")


def test_diagnostics_keep_message_and_project_frames_only(tmp_path):
    result = {"compiled": True, "visible": maven.parse_report(write(tmp_path))}
    d = maven.diagnostics(result)
    assert "Tests run: 3, Failures: 2" in d
    assert "expected: <3> but was: <2>" in d
    assert "at bench.Foo.add(Foo.java:27)" in d
    assert "AssertionUtils" not in d and "Method.invoke" not in d


def test_diagnostics_for_compile_failure_and_timeout():
    assert "cannot find symbol" in maven.diagnostics({"compiled": False, "compile_errors": "Foo.java:[3,5] cannot find symbol"})
    assert "timed out" in maven.diagnostics({"compiled": True, "timeout": True})


def test_compile_errors_strip_workspace_path():
    ws = "/tmp/ws123"
    out = "[INFO] building\n[ERROR] /tmp/ws123/src/main/java/bench/Foo.java:[3,5] cannot find symbol\n[ERROR] -> [Help 1]"
    assert maven.compile_errors(out, ws) == "[ERROR] src/main/java/bench/Foo.java:[3,5] cannot find symbol"
