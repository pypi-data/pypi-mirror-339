import pytest

import test.mock.uv
from uv_ci_tools.app.get_executable import app
from uv_ci_tools.lib import ci, util

from ._util import ExecutableContext


def run_app(ci_type: ci.Type = ci.Type.GITLAB, project_name: str | None = 'project_name'):
    with (
        util.set_env('CI_PROJECT_PATH', 'project_path'),
        util.set_env('CI_COMMIT_REF_NAME', 'commit_ref_name'),
        util.set_env('CI_SERVER_HOST', 'server_host'),
    ):
        app.get_executable(ci_type=ci_type, project_name=project_name)


def test_simple(capsys: pytest.CaptureFixture[str]):
    with ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)

        with test.mock.uv.set_uv_tool_list_show_paths_output(
            'project_name v0.0.0 (/)\n- tool (executable_path)'
        ):
            run_app()
    assert capsys.readouterr().out == 'executable_path'


def test_no_tool_installed():
    with ExecutableContext.make() as exe_ctx:
        exe_ctx.add_executable(test.mock.uv)

        with (
            test.mock.uv.set_uv_tool_list_show_paths_output('project_name v0.0.0 (/)'),
            pytest.raises(RuntimeError, match='No executable available'),
        ):
            run_app()
