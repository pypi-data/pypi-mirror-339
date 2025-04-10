import sys

from uv_ci_tools.lib import ci, cli, uv

APP = cli.sub_app(__name__)


@APP.default
def get_executable(*, ci_type: ci.Type = ci.Type.GITLAB, project_name: str | None = None):
    ci_ctx = ci_type.fill_context(ci.PartialContext(project_name=project_name))
    installed_package = uv.get_installed_package(ci_ctx.project_name)

    first_tool = next(iter(installed_package.tools), None)
    if first_tool is None:
        msg = f'No executable available for {project_name}'
        raise RuntimeError(msg)

    sys.stdout.write(str(first_tool.path))
