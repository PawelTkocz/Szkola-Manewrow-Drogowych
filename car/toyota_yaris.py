import math
from car.model import CarModelSpecification

TOYOTA_YARIS_SPECIFICATION: CarModelSpecification = {
    "name": "Toyota Yaris",
    "motion": {
        "acceleration": 0.07,
        "brake": 0.1,
        "max_velocity": 6,
        "resistance": 0.015,
    },
    "chassis": {"length": 90, "width": 50},
    "lights": {
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
        "turn_signals_tick_interval": 12,
    },
    "wheels": {"length": 22.5, "width": 6.25},
    "steering_system": {"wheels_max_angle": math.pi / 4, "wheels_turn_speed": 0.05},
    "body": {
        "shell": [
            {"x": -22.5, "y": -6},
            {"x": 22.5, "y": -6},
            {"x": 22.5, "y": -87.5},
            {"x": -22.5, "y": -87.5},
        ],
        "left_side_mirror": [
            {"x": -25, "y": -22.5},
            {"x": -25, "y": -27},
            {"x": -31.25, "y": -27},
            {"x": -31.25, "y": -22.5},
        ],
        "right_side_mirror": [
            {"x": 25, "y": -22.5},
            {"x": 31.25, "y": -22.5},
            {"x": 31.25, "y": -27},
            {"x": 25, "y": -27},
        ],
        "front_window": [
            {"x": -18.75, "y": -25.7},
            {"x": 18.75, "y": -25.7},
            {"x": 12.5, "y": -38.6},
            {"x": -12.5, "y": -38.6},
        ],
        "rear_window": [
            {"x": -12.5, "y": -77.1},
            {"x": 12.5, "y": -77.1},
            {"x": 6.25, "y": -70.7},
            {"x": -6.25, "y": -70.7},
        ],
        "left_window": [
            {"x": -18.75, "y": -36},
            {"x": -12.5, "y": -42},
            {"x": -12.5, "y": -66},
            {"x": -18.75, "y": -72},
        ],
        "right_window": [
            {"x": 12.5, "y": -42},
            {"x": 18.75, "y": -36},
            {"x": 18.75, "y": -72},
            {"x": 12.5, "y": -66},
        ],
    },
}
