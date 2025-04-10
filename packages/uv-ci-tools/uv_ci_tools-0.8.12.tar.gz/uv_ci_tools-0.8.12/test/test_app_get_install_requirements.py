import os

import pytest

import test.projects
from uv_ci_tools.app.get_install_requirement import app
from uv_ci_tools.lib import util


def run_app(project_name: str):
    with util.make_tmp_dir_copy(util.module_path(test.projects) / project_name) as project_dir:
        os.chdir(project_dir)
        app.get_install_requirement()


def test_simple(capsys: pytest.CaptureFixture[str]):
    run_app('simple')
    assert capsys.readouterr().out == 'simple==0.1.0'
