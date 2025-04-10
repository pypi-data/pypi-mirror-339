import subprocess

from uv_ci_tools.lib import ci, cli, util, uv

APP = cli.sub_app(__name__)


@APP.default
def pre_compile(*, ci_type: ci.Type = ci.Type.GITLAB, project_name: str | None = None):
    ci_ctx = ci_type.fill_context(ci.PartialContext(project_name=project_name))
    installed_package = uv.get_installed_package(ci_ctx.project_name)
    with util.devnull() as devnull:
        subprocess.run(
            [installed_package.python_executable, '-m', 'compileall', installed_package.path],
            check=True,
            stdout=devnull,
        )
