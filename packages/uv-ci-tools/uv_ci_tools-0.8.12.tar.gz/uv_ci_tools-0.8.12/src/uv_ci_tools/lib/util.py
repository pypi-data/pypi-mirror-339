import contextlib
import os
import pathlib
import shutil
import subprocess
import tempfile
import typing


def get_exe_path(name: str):
    exe_path = shutil.which(name)
    if exe_path is None:
        msg = f'Cannot find {name} executable'
        raise RuntimeError(msg)
    subprocess.run([exe_path, '--version'], capture_output=True, check=True)
    return pathlib.Path(exe_path)


def get_env_var(name: str):
    value = os.getenv(name, '')
    if len(value) == 0:
        msg = f'{name} is not set'
        raise RuntimeError(msg)
    return value


class HasDunderFile(typing.Protocol):
    @property
    def __file__(self) -> str: ...


def module_path(module: HasDunderFile):
    return pathlib.Path(module.__file__).parent.absolute()


@contextlib.contextmanager
def make_tmp_dir(base: pathlib.Path | None = None):
    with tempfile.TemporaryDirectory(dir=base) as tmp_dir:
        yield pathlib.Path(tmp_dir).absolute()


@contextlib.contextmanager
def make_tmp_dir_copy(dir_path: pathlib.Path):
    with make_tmp_dir(dir_path.parent) as tmp_dir:
        tmp_dir_copy_path = tmp_dir / dir_path.name
        shutil.copytree(dir_path, tmp_dir_copy_path)
        yield tmp_dir_copy_path


@contextlib.contextmanager
def set_env(name: str, value: object):
    old_value = os.getenv(name)
    if value is not None:
        os.environ[name] = str(value)
    elif old_value is not None:
        del os.environ[name]
    try:
        yield
    finally:
        if old_value is not None:
            os.environ[name] = old_value
        elif value is not None:
            del os.environ[name]


class PathLike[T](typing.Protocol):
    def __fspath__(self) -> T: ...


type StrOrBytesPath = str | bytes | PathLike[str] | PathLike[bytes]


def is_file(path: pathlib.Path):
    return path.exists() and path.is_file()


def is_executable(path: pathlib.Path):
    return is_file(path) and os.access(path, os.X_OK)


@contextlib.contextmanager
def devnull():
    with pathlib.Path(os.devnull).open(mode='w') as f:
        yield f


@contextlib.contextmanager
def use_contexts[T](
    contexts: list[contextlib.AbstractContextManager[T]],
) -> typing.Generator[list[T], None, None]:
    with contextlib.ExitStack() as stack:
        yield [stack.enter_context(cm) for cm in contexts]
