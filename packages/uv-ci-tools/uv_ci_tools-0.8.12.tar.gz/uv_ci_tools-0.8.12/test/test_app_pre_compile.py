import pytest

import test.mock.python
import test.mock.uv
from uv_ci_tools.app.pre_compile import app
from uv_ci_tools.lib import ci, util

from ._util import ExecutableContext


def run_app(ci_type: ci.Type = ci.Type.GITLAB, project_name: str | None = 'project_name'):
    with (
        util.set_env('CI_PROJECT_PATH', 'project_path'),
        util.set_env('CI_COMMIT_REF_NAME', 'commit_ref_name'),
        util.set_env('CI_SERVER_HOST', 'server_host'),
    ):
        app.pre_compile(ci_type=ci_type, project_name=project_name)


def test_simple(capsys: pytest.CaptureFixture[str]):
    with util.make_tmp_dir() as install_path, ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)
        python_executable = exe_ctx.add_executable(test.mock.python)

        bin_install_dir = install_path / 'bin'
        bin_install_dir.mkdir()
        installed_python_executable = bin_install_dir / 'python'
        installed_python_executable.symlink_to(python_executable)

        with test.mock.uv.set_uv_tool_list_show_paths_output(
            f'project_name v0.0.0 ({install_path})'
        ):
            run_app()
    assert 'compileall' not in capsys.readouterr().out


def test_not_installed():
    with ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)

        with (
            test.mock.uv.set_uv_tool_list_show_paths_output(''),
            pytest.raises(RuntimeError, match='Cannot find installed package'),
        ):
            run_app()


def test_no_python_executable():
    with util.make_tmp_dir() as install_path, ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)

        with (
            test.mock.uv.set_uv_tool_list_show_paths_output(
                f'project_name v0.0.0 ({install_path})'
            ),
            pytest.raises(RuntimeError, match='Canont find python executable'),
        ):
            run_app()
