from enum import Enum, auto
from dataclasses import dataclass


class ASSIGNMENT_STATE(Enum):
    ALIVE = 1
    DEAD = 2

    def __str__(self):
        return self.name
