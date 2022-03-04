from enum import Enum, auto
from dataclasses import dataclass


class SUBMISSION_STATE(Enum):
    NORMAL = 1
    DANGER = 2
    SUBMITTED = 3
    EXPIRED = 4

    def __str__(self):
        return self.name
