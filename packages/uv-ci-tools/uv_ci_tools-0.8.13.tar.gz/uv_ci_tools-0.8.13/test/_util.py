import contextlib
import dataclasses
import os
import pathlib
import sys

from uv_ci_tools.lib import util


@dataclasses.dataclass
class ExecutableContext:
    dir: pathlib.Path

    @staticmethod
    @contextlib.contextmanager
    def make():
        with util.make_tmp_dir() as tmp_dir, util.set_env('PATH', tmp_dir):
            yield ExecutableContext(tmp_dir)

    def add_executable(self, script: util.HasDunderFile):
        script_path = pathlib.Path(script.__file__)
        executable_path = self.dir / script_path.stem
        executable_path.write_text(
            '\n'.join(['#!/bin/bash', f'{sys.executable} {script_path} "$@"', ''])
        )
        executable_path.chmod(0o555)
        return executable_path


@contextlib.contextmanager
def remove_gitlab_ci_vars():
    with util.use_contexts([util.set_env(var, '') for var in os.environ if var.startswith('CI_')]):
        yield
