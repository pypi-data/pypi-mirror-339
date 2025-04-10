import enum

from . import gitlab
from .base import Context, PartialContext


class Type(enum.Enum):
    GITLAB = 'gitlab'

    def fill_context(self, partial: PartialContext):
        match self:
            case Type.GITLAB:  # pragma: no branch
                return gitlab.fill_context(partial)


__all__ = ['Context', 'PartialContext', 'Type']
