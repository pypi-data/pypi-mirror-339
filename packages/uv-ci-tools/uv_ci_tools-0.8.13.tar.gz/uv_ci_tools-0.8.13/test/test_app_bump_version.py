import os
import pathlib

import pytest

import test.mock
import test.mock.git
import test.mock.uv
import test.projects
from uv_ci_tools.app.bump_version import app
from uv_ci_tools.lib import ci, util, ver

from ._util import ExecutableContext, remove_gitlab_ci_vars


def run_app(
    project_name: str,
    *,
    increment_kind: ver.IncrementKind = ver.IncrementKind.PATCH,
    ci_type: ci.Type = ci.Type.GITLAB,
    disable_uv: bool = False,
    disable_git: bool = False,
    disable_project_name: bool = False,
    project_path: str | None = 'project_path',
    commit_ref_name: str | None = 'commit_ref_name',
    email: str | None = 'email',
    username: str | None = 'username',
    password: str | None = 'password',
    repository_host: str | None = 'repository_host',
):
    with (
        util.make_tmp_dir_copy(util.module_path(test.projects) / project_name) as project_dir,
        ExecutableContext.make() as exe_ctx,
    ):
        os.chdir(project_dir)

        if not disable_git:
            exe_ctx.add_executable(test.mock.git)
        if not disable_uv:
            exe_ctx.add_executable(test.mock.uv)

        app.version(
            increment_kind,
            ci_type=ci_type,
            project_name=project_name if not disable_project_name else None,
            project_path=project_path,
            commit_ref_name=commit_ref_name,
            email=email,
            username=username,
            password=password,
            repository_host=repository_host,
        )
        return test.mock.git.get_state(project_dir)


def test_simple():
    git_state = run_app('simple')
    assert git_state == test.mock.git.State(
        user_name='username',
        user_email='email',
        remote_name_url_map={
            'origin': 'https://username:password@repository_host/project_path.git'
        },
        staged_files={},
        commits=[],
        pushed=[
            test.mock.git.Pushed(
                commit=test.mock.git.Commit(
                    message='Bumped version to 0.1.1',
                    files={
                        pathlib.Path(
                            'pyproject.toml'
                        ): '[project]\nname = "simple"\nversion = "0.1.1"\n',
                        pathlib.Path('uv.lock'): '',
                    },
                ),
                repository='origin',
                refspec='HEAD:commit_ref_name',
                option='ci.skip',
            )
        ],
    )


def test_cannot_find_git():
    with pytest.raises(RuntimeError, match='Cannot find git'):
        run_app('simple', disable_git=True)


def test_cannot_find_uv():
    with pytest.raises(RuntimeError, match='Cannot find uv'):
        run_app('simple', disable_uv=True)


def test_gitlab_no_project_name():
    with remove_gitlab_ci_vars(), pytest.raises(RuntimeError, match='CI_PROJECT_NAME'):
        run_app('simple', ci_type=ci.Type.GITLAB, disable_project_name=True)


def test_gitlab_project_name_with_env():
    with util.set_env('CI_PROJECT_NAME', 'project_name'):
        git_state = run_app(
            'simple', ci_type=ci.Type.GITLAB, disable_project_name=True, username=None
        )
    assert git_state.user_name == 'project_name-ci'


def test_gitlab_no_project_path():
    with remove_gitlab_ci_vars(), pytest.raises(RuntimeError, match='CI_PROJECT_PATH'):
        run_app('simple', ci_type=ci.Type.GITLAB, project_path=None)


def test_gitlab_no_commit_ref_name():
    with remove_gitlab_ci_vars(), pytest.raises(RuntimeError, match='CI_COMMIT_REF_NAME'):
        run_app('simple', commit_ref_name=None)


def test_gitlab_no_repository_host():
    with remove_gitlab_ci_vars(), pytest.raises(RuntimeError, match='CI_SERVER_HOST'):
        run_app('simple', repository_host=None)


def test_gitlab_no_email():
    git_state = run_app('simple', email=None)
    assert git_state.user_email == 'username@repository_host'


def test_gitlab_no_username():
    git_state = run_app('simple', username=None)
    assert git_state.user_name == 'simple-ci'


def test_gitlab_no_password():
    with pytest.raises(RuntimeError, match='password'):
        run_app('simple', password=None)
