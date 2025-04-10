import sys
import typing

from uv_ci_tools.lib import cli, pyproject, uv

APP = cli.sub_app(__name__)


def get_project():
    return pyproject.get_project(pyproject.get_document())


def get_project_name():
    return pyproject.get_project_name(get_project())


def get_project_version():
    return pyproject.get_project_version(get_project())


type Key = typing.Literal['project-version', 'project-name', 'installed-executable']


@APP.default
def get(key: Key, /):
    match key:
        case 'project-version':
            text = get_project_version().dump()
        case 'project-name':
            text = get_project_name()
        case 'installed-executable':  # pragma: no branch
            project_name = get_project_name()
            installed_package = uv.get_installed_package(project_name)
            first_tool = next(iter(installed_package.tools), None)
            if first_tool is None:
                msg = f'No executable available for {project_name}'
                raise RuntimeError(msg)
            text = str(first_tool.path)

    sys.stdout.write(text)
