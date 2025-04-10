import pathlib
import typing

import cyclopts

APP = cyclopts.App()


@APP.command
def commit(
    _: typing.Annotated[typing.Literal['compileall'], cyclopts.Parameter(name=['-m'])],
    directory: pathlib.Path,
):
    print('compileall')
    (directory / '__pycache__').mkdir()
