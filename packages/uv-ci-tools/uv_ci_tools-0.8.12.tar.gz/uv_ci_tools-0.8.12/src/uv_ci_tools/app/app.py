from uv_ci_tools.lib import cli

from . import bump_version, get_executable, get_install_requirement, pre_compile

APP = cli.main_app()

APP.command(bump_version.APP)
APP.command(pre_compile.APP)
APP.command(get_executable.APP)
APP.command(get_install_requirement.APP)
