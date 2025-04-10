import dataclasses


@dataclasses.dataclass
class PartialContext:
    project_name: str | None = None
    project_path: str | None = None
    commit_ref_name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    repository_host: str | None = None


@dataclasses.dataclass
class Context:
    project_name: str
    project_path: str
    commit_ref_name: str
    email: str
    username: str
    password: str | None
    repository_host: str
