import pathlib
import typing

import tomlkit.items
import tomlkit.toml_document

from uv_ci_tools.lib import ver


def get_path():
    return pathlib.Path('pyproject.toml')


def get_document():
    pyproject_path = get_path()
    return tomlkit.parse(pyproject_path.read_text())


def set_document(document: tomlkit.toml_document.TOMLDocument):
    get_path().write_text(document.as_string())


def get_project(document: tomlkit.toml_document.TOMLDocument):
    project_item = document['project']
    assert isinstance(project_item, tomlkit.items.Table)
    return project_item


def get_project_version(project: tomlkit.items.Table):
    version_item = project['version']
    assert isinstance(version_item, tomlkit.items.String)
    return ver.Version.load(version_item)


def set_project_version(project: tomlkit.items.Table, version: ver.Version):
    project['version'] = version.dump()


def get_project_name(project: tomlkit.items.Table):
    name_item = project['name']
    assert isinstance(name_item, tomlkit.items.String)
    return name_item


def update_version(version_action: typing.Callable[[ver.Version], ver.Version]):
    document = get_document()
    project = get_project(document)
    old_version = get_project_version(project)
    new_version = version_action(old_version)
    set_project_version(project, new_version)
    set_document(document)
    return new_version
