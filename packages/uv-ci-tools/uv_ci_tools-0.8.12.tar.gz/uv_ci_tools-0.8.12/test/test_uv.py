import pathlib

import test.mock.uv
from uv_ci_tools.lib import uv, ver

from ._util import ExecutableContext


def test_parse_tool_list_show_paths():
    with (
        test.mock.uv.set_uv_tool_list_show_paths_output(
            """\
- tool0 (/)
pkg1 v0.1.2 (a)
pkg2 v1.0.0 (b/c)
- tool1 (/d/e/f)
pkg3 v0.0.1 (/g)
- tool2 (/)
- tool3 (h)
- tool0
pkg0 v0 (/g)
pkg0 v0.0.0
"""
        ),
        ExecutableContext.make() as exe_ctx,
    ):
        exe_ctx.add_executable(test.mock.uv)
        assert uv.list_installed_packages() == [
            uv.InstalledPackage('pkg1', ver.Version(0, 1, 2), pathlib.Path('a'), tools=[]),
            uv.InstalledPackage(
                'pkg2',
                ver.Version(1, 0, 0),
                pathlib.Path('b/c'),
                tools=[uv.InstalledTool('tool1', pathlib.Path('/d/e/f'))],
            ),
            uv.InstalledPackage(
                'pkg3',
                ver.Version(0, 0, 1),
                pathlib.Path('/g'),
                tools=[
                    uv.InstalledTool('tool2', pathlib.Path('/')),
                    uv.InstalledTool('tool3', pathlib.Path('h')),
                ],
            ),
        ]
