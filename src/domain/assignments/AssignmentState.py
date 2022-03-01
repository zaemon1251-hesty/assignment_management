from enum import Enum, auto
from dataclasses import dataclass


class ASSIGNMENT_STATE(Enum):
    ALIVE = auto()
    END = auto()

    def __str__(self):
        return self.name


@dataclass(init=False, eq=True, frozen=True)
class assignment_state:
    """assignment_state represents how hot the selected course is. """

    value: ASSIGNMENT_STATE

    def __init__(self, value: str):
        object.__setattr__(self, "value", value)
