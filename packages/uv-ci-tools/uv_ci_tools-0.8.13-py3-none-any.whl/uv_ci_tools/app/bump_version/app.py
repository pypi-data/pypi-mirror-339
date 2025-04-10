from uv_ci_tools.lib import ci, cli, git, pyproject, uv, ver

APP = cli.sub_app(__name__)


@APP.default
def version(
    increment_kind: ver.IncrementKind,
    /,
    *,
    ci_type: ci.Type = ci.Type.GITLAB,
    project_name: str | None = None,
    project_path: str | None = None,
    commit_ref_name: str | None = None,
    email: str | None = None,
    username: str | None = None,
    password: str | None = None,
    repository_host: str | None = None,
):
    ci_ctx = ci_type.fill_context(
        ci.PartialContext(
            project_name=project_name,
            project_path=project_path,
            commit_ref_name=commit_ref_name,
            email=email,
            username=username,
            password=password,
            repository_host=repository_host,
        )
    )
    new_version = pyproject.update_version(lambda version: version.incremented(increment_kind))
    uv.update_lock_file()
    git.push(
        pyproject.get_path(),
        uv.get_lock_file_path(),
        message=f'Bumped version to {new_version.dump()}',
        ci_ctx=ci_ctx,
    )
