from typing import TypeAlias, TypedDict


class CarPointPosition(TypedDict):
    """
    Representation of a point on a car.

    The (0, 0) point is the point in the middle of front bumper
    (the car is directed UP, horizontally to the Y axis).
    """

    x: float
    y: float


# Position of a car part can be defined as list of points creating polygon
CarPartPosition: TypeAlias = list[CarPointPosition]


class SymmetricCarPartPositions(TypedDict):
    left: CarPartPosition
    right: CarPartPosition


class WheelPosition(TypedDict):
    middle: CarPointPosition
    corners: CarPartPosition


class WheelsPositions(TypedDict):
    left: WheelPosition
    right: WheelPosition


class WheelsSize(TypedDict):
    length: float
    width: float


class WindowsPosition(SymmetricCarPartPositions):
    front: CarPartPosition
    rear: CarPartPosition


class CarModelAppearance(TypedDict):
    length: float
    width: float
    shell: CarPartPosition
    wheels: WheelsSize
    front_lights: SymmetricCarPartPositions
    side_mirrors: SymmetricCarPartPositions
    windows: WindowsPosition


class CarModelSpecification(TypedDict):
    max_wheels_turn: float
    wheels_turn_speed: float
    max_velocity: float
    max_acceleration: float
    max_brake: float
    resistance: float


class CarModel:
    def __init__(
        self,
        name: str,
        specification: CarModelSpecification,
        appearance: CarModelAppearance,
    ):
        self.name = name
        self.specification = specification
        self.appearance = appearance
        self.wheels_positions = self._get_wheels_positions()

    def _get_wheels_positions(self) -> WheelsPositions:
        car_width = self.appearance["width"]
        wheel_width = self.appearance["wheels"]["width"]
        wheel_length = self.appearance["wheels"]["length"]
        return {
            "left": {
                "middle": {
                    "x": -1 * (car_width / 2 - wheel_width / 2),
                    "y": -0.5 * wheel_length,
                },
                "corners": [
                    {"x": -1 * car_width / 2, "y": 0},
                    {"x": -1 * (car_width / 2 - wheel_width), "y": 0},
                    {"x": -1 * (car_width / 2 - wheel_width), "y": -1 * wheel_length},
                    {"x": -1 * car_width / 2, "y": -1 * wheel_length},
                ],
            },
            "right": {
                "middle": {
                    "x": car_width / 2 - wheel_width / 2,
                    "y": -0.5 * wheel_length,
                },
                "corners": [
                    {"x": car_width / 2 - wheel_width, "y": 0},
                    {"x": car_width / 2, "y": 0},
                    {"x": car_width / 2, "y": -1 * wheel_length},
                    {"x": car_width / 2 - wheel_width, "y": -1 * wheel_length},
                ],
            },
        }

    @property
    def width(self):
        return self.appearance["width"]

    @property
    def length(self):
        return self.appearance["length"]

    @property
    def max_wheels_turn(self):
        return self.specification["max_wheels_turn"]

    @property
    def wheels_turn_speed(self):
        return self.specification["wheels_turn_speed"]

    @property
    def max_velocity(self):
        return self.specification["max_velocity"]

    @property
    def max_acceleration(self):
        return self.specification["max_acceleration"]

    @property
    def max_brake(self):
        return self.specification["max_brake"]

    @property
    def resistance(self):
        return self.specification["resistance"]
