
from enum import Enum

class NamedEnum(Enum):
    @classmethod
    def get_name(cls, val: int) -> str:
        n = ''
        for e in cls:
            if e.value == val:
                n = e.name
                break
        return n
