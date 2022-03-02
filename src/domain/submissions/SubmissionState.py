from enum import Enum, auto
from dataclasses import dataclass


class SUBMISSION_STATE(Enum):
    NORMAL = 1
    DANGER = 2
    SUBMITTED = 3
    EXPIRED = 4

    def __str__(self):
        return self.name


@dataclass(init=False, eq=True, frozen=True)
class submission_state:
    """submission_state represents how hot the selected course is. """

    value: SUBMISSION_STATE

    def __init__(self, value: str):
        object.__setattr__(self, "value", value)
