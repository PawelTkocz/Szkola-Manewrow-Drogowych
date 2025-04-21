from enum import Enum
from drafter.drawable import Drawable


class TrafficSignName(Enum):
    A5 = "A5"
    D1 = "D1"
    A7 = "A7"
    B20 = "B20"
    T6a = "T6a"
    T6c = "T6c"


class TrafficSign(Drawable):
    def __init__(self, name: TrafficSignName) -> None:
        self.name = name
