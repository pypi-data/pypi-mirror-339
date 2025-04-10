"""Test the CLI entrypoint, argument parsing and error printing."""

import contextlib
import dataclasses
import sys

import pytest

import uv_ci_tools
from uv_ci_tools import __main__

type _Capsys = pytest.CaptureFixture[str]


@dataclasses.dataclass
class _Console:
    out: str
    err: str


@contextlib.contextmanager
def _setup(argv: list[object], capsys: _Capsys):
    previous_argv = sys.argv
    sys.argv = [sys.executable, *(map(str, argv))]
    console = _Console(out='', err='')
    capsys.readouterr()  # clears buffer
    try:
        yield console
    finally:
        capture = capsys.readouterr()
        console.out = capture.out
        console.err = capture.err
        sys.argv = previous_argv


def test_main_version(capsys: _Capsys) -> None:
    with _setup(['--version'], capsys) as console:
        __main__.main()

    assert console.out == uv_ci_tools.__version__ + '\n'
