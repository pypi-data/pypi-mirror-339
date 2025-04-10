import dataclasses
import enum
import typing


class IncrementKind(enum.Enum):
    MAJOR = 'major'
    MINOR = 'minor'
    PATCH = 'patch'


@dataclasses.dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def load(cls, value: str) -> typing.Self:
        if not value:
            msg = 'no value'
            raise RuntimeError(msg)

        parts = value.split('.')
        if len(parts) != len(dataclasses.fields(cls)):
            msg = f'should be 3 parts separated by dots: {value}'
            raise RuntimeError(msg)

        parts_int: list[int] = []
        for part in parts:
            try:
                parts_int.append(int(part))
            except ValueError as e:
                msg = f'parts should be integers: {value}'
                raise RuntimeError(msg) from e

        return cls(*parts_int)

    def dump(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}'

    def incremented(self, kind: IncrementKind) -> typing.Self:
        match kind:
            case IncrementKind.MAJOR:
                return self.__class__(major=self.major + 1, minor=0, patch=0)
            case IncrementKind.MINOR:
                return self.__class__(major=self.major, minor=self.minor + 1, patch=0)
            case _:
                return self.__class__(major=self.major, minor=self.minor, patch=self.patch + 1)
