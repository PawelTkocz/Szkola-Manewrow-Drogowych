import math
from car.model import CarModel, CarModelAppearance, CarModelSpecification


class ToyotaYaris(CarModel):
    name = "Toyota Yaris"
    specification: CarModelSpecification = {
        "max_acceleration": 0.07,
        "max_velocity": 6,
        "max_brake": 0.1,
        "max_wheels_turn": math.pi / 4,
        "resistance": 0.015,
        "wheels_turn_speed": 0.05,
        "turn_signals_tick_interval": 12,
    }
    appearance: CarModelAppearance = {
        "width": 50,
        "length": 90,
        "shell": [
            {"x": -22.5, "y": -6},
            {"x": 22.5, "y": -6},
            {"x": 22.5, "y": -87.5},
            {"x": -22.5, "y": -87.5},
        ],
        "wheels": {
            "length": 22.5,
            "width": 6.25,
        },
        "front_lights": {
            "left": [
                {"x": -25, "y": 0},
                {"x": -12.5, "y": 0},
                {"x": -12.5, "y": -6},
                {"x": -25, "y": -6},
            ],
            "right": [
                {"x": 12.5, "y": 0},
                {"x": 25, "y": 0},
                {"x": 25, "y": -6},
                {"x": 12.5, "y": -6},
            ],
        },
        "side_mirrors": {
            "left": [
                {"x": -25, "y": -22.5},
                {"x": -25, "y": -27},
                {"x": -31.25, "y": -27},
                {"x": -31.25, "y": -22.5},
            ],
            "right": [
                {"x": 25, "y": -22.5},
                {"x": 31.25, "y": -22.5},
                {"x": 31.25, "y": -27},
                {"x": 25, "y": -27},
            ],
        },
        "windows": {
            "front": [
                {"x": -18.75, "y": -25.7},
                {"x": 18.75, "y": -25.7},
                {"x": 12.5, "y": -38.6},
                {"x": -12.5, "y": -38.6},
            ],
            "rear": [
                {"x": -12.5, "y": -77.1},
                {"x": 12.5, "y": -77.1},
                {"x": 6.25, "y": -70.7},
                {"x": -6.25, "y": -70.7},
            ],
            "left": [
                {"x": -18.75, "y": -36},
                {"x": -12.5, "y": -42},
                {"x": -12.5, "y": -66},
                {"x": -18.75, "y": -72},
            ],
            "right": [
                {"x": 12.5, "y": -42},
                {"x": 18.75, "y": -36},
                {"x": 18.75, "y": -72},
                {"x": 12.5, "y": -66},
            ],
        },
    }

    def __init__(self) -> None:
        super().__init__(self.name, self.specification, self.appearance)
