import pytest

from repair.prompts import extract_java, initial_prompt, retry_prompt

BUGGY = "package bench;\npublic final class Foo { int f() { return 1; } }"
TEST = "class FooVisibleTest { @Test void t() {} }"


def test_baseline_prompt_has_code_and_test_but_no_diagnostics():
    p = initial_prompt("Foo", BUGGY, TEST, "baseline", diag="expected: <2> but was: <1>")
    assert BUGGY in p and TEST in p
    assert "expected: <2>" not in p
    assert "Test execution output" not in p


def test_diagnostics_prompt_adds_execution_output():
    p = initial_prompt("Foo", BUGGY, TEST, "diagnostics", diag="expected: <2> but was: <1>")
    assert BUGGY in p and TEST in p
    assert "expected: <2> but was: <1>" in p


def test_prompts_never_mention_hidden_tests():
    for cond in ("baseline", "diagnostics"):
        assert "Hidden" not in initial_prompt("Foo", BUGGY, TEST, cond, "x")
        assert "Hidden" not in retry_prompt("Foo", cond, True, "x")


def test_unknown_condition_rejected():
    with pytest.raises(ValueError):
        initial_prompt("Foo", BUGGY, TEST, "oracle")


def test_retry_prompt_only_shows_output_in_diagnostics_condition():
    assert "NullPointerException" not in retry_prompt("Foo", "baseline", True, "NullPointerException")
    assert "NullPointerException" in retry_prompt("Foo", "diagnostics", True, "NullPointerException")
    assert "does not compile" in retry_prompt("Foo", "baseline", False, "")


def test_extract_java_block():
    reply = "Here is the fix:\n```java\npublic final class Foo { int f() { return 2; } }\n```\nDone."
    assert extract_java(reply, "Foo") == "public final class Foo { int f() { return 2; } }\n"


def test_extract_prefers_block_declaring_the_class():
    reply = "```java\nint x = 1;\n```\n```java\nclass Foo {}\n```"
    assert extract_java(reply, "Foo") == "class Foo {}\n"


def test_extract_accepts_unlabelled_fence_and_crlf():
    assert extract_java("```\r\nclass Foo {}\r\n```", "Foo").strip() == "class Foo {}"


def test_extract_returns_none_without_matching_block():
    assert extract_java("no code here", "Foo") is None
    assert extract_java("```java\nclass FooBar {}\n```", "Foo") is None
    assert extract_java("```python\nclass Foo: pass\n```", "Foo") is None
    assert extract_java(None, "Foo") is None
