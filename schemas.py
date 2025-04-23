from enum import Enum


class HorizontalDirection(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class VerticalDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"


class CardinalDirection(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


class VehicleMovementDirection(Enum):
    FRONT = "FRONT"
    REVERSE = "REVERSE"
