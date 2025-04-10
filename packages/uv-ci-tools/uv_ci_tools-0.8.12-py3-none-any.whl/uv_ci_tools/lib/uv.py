import contextlib
import dataclasses
import functools
import pathlib
import subprocess

from uv_ci_tools.lib import util, ver


def get_lock_file_path():
    return pathlib.Path('uv.lock')


def update_lock_file():
    uv_exe_path = util.get_exe_path('uv')
    subprocess.run([uv_exe_path, 'lock'], check=True)


@dataclasses.dataclass
class InstalledTool:
    name: str
    path: pathlib.Path


@dataclasses.dataclass
class InstalledPackage:
    name: str
    version: ver.Version
    path: pathlib.Path
    tools: list[InstalledTool]

    @functools.cached_property
    def python_executable(self):
        python_executable = self.path / 'bin' / 'python'
        if not util.is_executable(python_executable):
            msg = f'Canont find python executable for package {self.name}'
            raise RuntimeError(msg)
        return python_executable


def list_installed_packages():
    uv_exe_path = util.get_exe_path('uv')
    process = subprocess.run(
        [uv_exe_path, 'tool', 'list', '--show-paths'], check=True, capture_output=True, text=True
    )
    assert process.stdout is not None
    packages: list[InstalledPackage] = []
    for line in process.stdout.splitlines():
        match line.split():
            case ['-', name, path_part]:
                last_package = next(reversed(packages), None)
                if last_package is not None:
                    path = pathlib.Path(path_part[1:-1])
                    last_package.tools.append(InstalledTool(name, path))
            case [name, version_part, path_part]:
                with contextlib.suppress(RuntimeError):
                    version = ver.Version.load(version_part[1:])
                    path = pathlib.Path(path_part[1:-1])
                    packages.append(InstalledPackage(name, version, path, tools=[]))
            case _:
                pass
    return packages


def get_installed_package(project_name: str):
    project_name_installed_package_map = {
        package.name: package for package in list_installed_packages()
    }
    installed_package = project_name_installed_package_map.get(project_name)
    if installed_package is None:
        msg = f'Cannot find installed package for {project_name}'
        raise RuntimeError(msg)
    return installed_package
