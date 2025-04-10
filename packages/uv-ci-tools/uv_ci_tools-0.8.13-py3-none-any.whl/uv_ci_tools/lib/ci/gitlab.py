from uv_ci_tools.lib import util

from . import base


def fill_context(partial: base.PartialContext):
    if partial.project_name is None:
        partial.project_name = util.get_env_var('CI_PROJECT_NAME')
    if partial.project_path is None:
        partial.project_path = util.get_env_var('CI_PROJECT_PATH')
    if partial.commit_ref_name is None:
        partial.commit_ref_name = util.get_env_var('CI_COMMIT_REF_NAME')
    if partial.repository_host is None:
        partial.repository_host = util.get_env_var('CI_SERVER_HOST')
    if partial.username is None:
        partial.username = f'{partial.project_name}-ci'
    if partial.email is None:
        partial.email = f'{partial.username}@{partial.repository_host}'
    return base.Context(
        project_name=partial.project_name,
        project_path=partial.project_path,
        commit_ref_name=partial.commit_ref_name,
        username=partial.username,
        password=partial.password,
        repository_host=partial.repository_host,
        email=partial.email,
    )
