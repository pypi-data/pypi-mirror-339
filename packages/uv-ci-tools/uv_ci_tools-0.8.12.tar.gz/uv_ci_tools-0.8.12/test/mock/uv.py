import base64
import contextlib
import os
import pathlib
import sys
import typing

import cyclopts

APP = cyclopts.App(version='0.1.0')


@APP.command
def lock() -> None:
    pathlib.Path('uv.lock').write_text('')


_UV_TOOL_LIST_SHOW_PATHS_B64_VAR = 'UV_TOOL_LIST_SHOW_PATHS_B64_VAR'


@contextlib.contextmanager
def set_uv_tool_list_show_paths_output(output: str):
    from uv_ci_tools.lib import util

    with util.set_env(_UV_TOOL_LIST_SHOW_PATHS_B64_VAR, base64.b64encode(output.encode()).decode()):
        yield


@APP.command
def tool(_: typing.Literal['list'], /, *, show_paths: bool = False) -> None:
    if show_paths:
        print(base64.b64decode(os.getenv(_UV_TOOL_LIST_SHOW_PATHS_B64_VAR, '')).decode())


if __name__ == '__main__':
    APP.__call__(sys.argv[1:], print_error=True, exit_on_error=False)
