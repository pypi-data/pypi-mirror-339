from uv_ci_tools.lib import cli

from . import bump_version, get, pre_compile

APP = cli.main_app()

APP.command(bump_version.APP)
APP.command(pre_compile.APP)
APP.command(get.APP)
