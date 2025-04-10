import os

import pytest

import test.mock.uv
import test.projects
from uv_ci_tools.app.get import app
from uv_ci_tools.lib import util

from ._util import ExecutableContext


def run_app(project_name: str, key: app.Key):
    with util.make_tmp_dir_copy(util.module_path(test.projects) / project_name) as project_dir:
        os.chdir(project_dir)
        app.get(key)


def test_simple_project_name(capsys: pytest.CaptureFixture[str]):
    run_app('simple', 'project-name')
    assert capsys.readouterr().out == 'simple'


def test_simple_project_version(capsys: pytest.CaptureFixture[str]):
    run_app('simple', 'project-version')
    assert capsys.readouterr().out == '0.1.0'


def test_simple_install_exectuable(capsys: pytest.CaptureFixture[str]):
    with ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)

        with test.mock.uv.set_uv_tool_list_show_paths_output(
            'simple v0.0.0 (/)\n- tool (executable_path)'
        ):
            run_app('simple', 'installed-executable')
    assert capsys.readouterr().out == 'executable_path'


def test_no_tool_installed():
    with ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)

        with (
            test.mock.uv.set_uv_tool_list_show_paths_output('simple v0.0.0 (/)'),
            pytest.raises(RuntimeError, match='No executable available'),
        ):
            run_app('simple', 'installed-executable')
