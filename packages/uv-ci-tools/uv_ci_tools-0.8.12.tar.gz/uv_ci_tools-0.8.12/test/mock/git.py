import contextlib
import pathlib
import sys
import typing

import cyclopts
import pydantic

APP = cyclopts.App()


class Commit(pydantic.BaseModel):
    message: str
    files: dict[pathlib.Path, str]


class Pushed(pydantic.BaseModel):
    commit: Commit
    repository: str
    refspec: str
    option: str


class State(pydantic.BaseModel):
    user_name: str | None = None
    user_email: str | None = None
    remote_name_url_map: dict[str, str] = pydantic.Field(default_factory=dict)
    staged_files: dict[pathlib.Path, str] = pydantic.Field(default_factory=dict)
    commits: list[Commit] = pydantic.Field(default_factory=list)
    pushed: list[Pushed] = pydantic.Field(default_factory=list)


def get_state_path(project_dir: pathlib.Path | None):
    if project_dir is None:
        project_dir = pathlib.Path.cwd()
    return project_dir / 'git_state.json'


def get_state(project_dir: pathlib.Path | None = None):
    try:
        text = get_state_path(project_dir=project_dir).read_text()
    except FileNotFoundError:
        text = '{}'
    return State.model_validate_json(text)


def set_state(state: State, project_dir: pathlib.Path | None = None):
    get_state_path(project_dir=project_dir).write_text(state.model_dump_json())


@contextlib.contextmanager
def sync_state():
    state = get_state()
    print(state)
    yield state
    set_state(state)


@APP.command
def config(key: typing.Literal['user.name', 'user.email'], value: str) -> None:
    with sync_state() as state:
        match key:
            case 'user.name':
                state.user_name = value
            case 'user.email':
                state.user_email = value


@APP.command
def remote(action: typing.Literal['remove', 'add'], name: str, url: str | None = None):
    with sync_state() as state:
        match action:
            case 'add':
                assert name not in state.remote_name_url_map
                assert url is not None
                state.remote_name_url_map[name] = url
            case 'remove':
                del state.remote_name_url_map[name]


@APP.command
def add(*paths: pathlib.Path):
    with sync_state() as state:
        state.staged_files.update({path: path.read_text() for path in paths})


@APP.command
def commit(*, message: typing.Annotated[str, cyclopts.Parameter(name=['-m'])]):
    with sync_state() as state:
        assert len(state.staged_files) > 0
        state.commits.append(Commit(message=message, files=state.staged_files))
        state.staged_files.clear()


@APP.command
def push(
    repository: str, refspec: str, *, option: typing.Annotated[str, cyclopts.Parameter(name=['-o'])]
):
    with sync_state() as state:
        assert len(state.commits) > 0
        for commit in state.commits:
            state.pushed.append(
                Pushed(commit=commit, repository=repository, refspec=refspec, option=option)
            )
        state.commits.clear()


if __name__ == '__main__':
    APP.__call__(sys.argv[1:], print_error=True, exit_on_error=False)
