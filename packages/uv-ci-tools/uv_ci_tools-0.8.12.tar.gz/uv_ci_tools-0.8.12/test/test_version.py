import pytest

from uv_ci_tools.lib import ver


def test_load():
    with pytest.raises(RuntimeError, match='no value'):
        ver.Version.load('')

    with pytest.raises(RuntimeError, match='3 parts'):
        ver.Version.load('1.2.3.4')

    with pytest.raises(RuntimeError, match='3 parts'):
        ver.Version.load('1.2')

    with pytest.raises(RuntimeError, match='integer'):
        ver.Version.load('1.2.a')

    assert ver.Version.load('1.2.3') == ver.Version(1, 2, 3)


def test_dump():
    assert ver.Version.load('1.2.3').dump() == '1.2.3'


def test_major() -> None:
    major = ver.IncrementKind.MAJOR
    assert ver.Version(1, 0, 0).incremented(major) == ver.Version(2, 0, 0)
    assert ver.Version(2, 57, 2).incremented(major) == ver.Version(3, 0, 0)
    assert ver.Version(0, 0, 0).incremented(major) == ver.Version(1, 0, 0)
    assert ver.Version(0, 0, 17).incremented(major) == ver.Version(1, 0, 0)


def test_minor() -> None:
    minor = ver.IncrementKind.MINOR
    assert ver.Version(1, 0, 0).incremented(minor) == ver.Version(1, 1, 0)
    assert ver.Version(1, 12, 0).incremented(minor) == ver.Version(1, 13, 0)
    assert ver.Version(3, 0, 5).incremented(minor) == ver.Version(3, 1, 0)
    assert ver.Version(0, 3, 0).incremented(minor) == ver.Version(0, 4, 0)
    assert ver.Version(0, 0, 2).incremented(minor) == ver.Version(0, 1, 0)


def test_patch() -> None:
    patch = ver.IncrementKind.PATCH
    assert ver.Version(1, 0, 0).incremented(patch) == ver.Version(1, 0, 1)
    assert ver.Version(5, 37, 0).incremented(patch) == ver.Version(5, 37, 1)
    assert ver.Version(0, 0, 0).incremented(patch) == ver.Version(0, 0, 1)
    assert ver.Version(0, 0, 99).incremented(patch) == ver.Version(0, 0, 100)
