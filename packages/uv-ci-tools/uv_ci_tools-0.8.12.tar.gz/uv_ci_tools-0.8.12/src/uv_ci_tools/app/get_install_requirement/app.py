import sys

from uv_ci_tools.lib import cli, pyproject

APP = cli.sub_app(__name__)


@APP.default
def get_install_requirement():
    project = pyproject.get_project(pyproject.get_document())
    project_name = pyproject.get_project_name(project)
    project_version = pyproject.get_project_version(project)
    sys.stdout.write(f'{project_name}=={project_version.dump()}')
