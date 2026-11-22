"""Prompts for the two experimental conditions and extraction of the patched class."""
import re

CONDITIONS = ("baseline", "diagnostics")

SYSTEM = "You are an experienced Java developer. You fix bugs with minimal, correct changes."

_FORMAT = ("Return the complete corrected `{cls}.java` in a single ```java code block. "
           "Keep the package, the class name and the public API unchanged. Do not modify the tests.")


def initial_prompt(cls, buggy_src, visible_test_src, condition, diag=""):
    """Baseline: buggy code + failing test. Diagnostics: the same plus the test execution output."""
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition {condition!r}")
    parts = [
        f"The Java class `{cls}` below contains a bug. Its Javadoc describes the intended behaviour. "
        f"The JUnit 5 test class `{cls}VisibleTest` fails against it.",
        f"### {cls}.java\n```java\n{buggy_src.strip()}\n```",
        f"### {cls}VisibleTest.java\n```java\n{visible_test_src.strip()}\n```",
    ]
    if condition == "diagnostics":
        parts.append(f"### Test execution output\n```\n{diag.strip()}\n```")
    parts.append(_FORMAT.format(cls=cls))
    return "\n\n".join(parts)


def retry_prompt(cls, condition, compiled, diag=""):
    """Feedback after a failed attempt; only the diagnostics condition sees the new output."""
    msg = "Your corrected class does not compile." if not compiled else "The test still fails with your corrected class."
    if condition == "diagnostics":
        msg += f"\n\n### Test execution output\n```\n{diag.strip()}\n```"
    return msg + "\n\nPlease try again. " + _FORMAT.format(cls=cls)


_BLOCK = re.compile(r"```[ \t]*([A-Za-z]*)[ \t]*\r?\n(.*?)```", re.S)


def extract_java(reply, cls):
    """Return the code block that declares `cls` (preferring ```java blocks), or None."""
    blocks = [(lang.lower(), body.strip()) for lang, body in _BLOCK.findall(reply or "")]
    declares = re.compile(rf"\b(class|record|enum|interface)\s+{re.escape(cls)}\b")
    candidates = [b for lang, b in blocks if declares.search(b) and lang in ("java", "")]
    return candidates[0] + "\n" if candidates else None
