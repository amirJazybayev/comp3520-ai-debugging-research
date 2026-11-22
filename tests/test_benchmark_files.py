"""Static checks on the benchmark layout (no Maven needed)."""
import re

import pytest

from repair import maven

BUGS = maven.load_bugs()


def test_fifteen_unique_bugs():
    assert len(BUGS) == 15
    assert len({b["id"] for b in BUGS}) == len({b["class"] for b in BUGS}) == 15


@pytest.mark.parametrize("bug", BUGS, ids=[b["id"] for b in BUGS])
def test_bug_has_all_files_and_a_real_fault(bug):
    cls = bug["class"]
    assert (maven.TESTS / f"{cls}VisibleTest.java").exists()
    assert (maven.TESTS / f"{cls}HiddenTest.java").exists()
    buggy, ref = maven.buggy_source(bug), maven.reference_source(bug)
    assert buggy != ref
    assert re.search(rf"public final class {cls}\b", buggy)
    # the specification (Javadoc) given to the model must be identical to the reference's
    javadoc = re.compile(r"/\*\*.*?\*/", re.S)
    assert javadoc.findall(buggy) == javadoc.findall(ref)


@pytest.mark.parametrize("bug", BUGS, ids=[b["id"] for b in BUGS])
def test_hidden_tests_are_more_thorough_than_visible(bug):
    count = lambda name: (maven.TESTS / name).read_text(encoding="utf-8").count("@Test")
    assert count(f"{bug['class']}HiddenTest.java") > count(f"{bug['class']}VisibleTest.java")
