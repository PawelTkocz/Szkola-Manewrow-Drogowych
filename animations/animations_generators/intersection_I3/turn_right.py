from animations.animations_generators.constants import (
    PRIMARY_CAR_COLOR,
    SECONDARY_CAR_COLOR,
)
from animations.animations_generators.intersection_I3.intersection_I3_animations import (
    IntersectionI3Animation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from car.toyota_yaris_specification import TOYOTA_YARIS_SPECIFICATION
from schemas import CardinalDirection

MANOEUVRE_CONTROL_INSTRUCTIONS_DIR_NAME = "turn_right"
CARS_DESCRIPTIONS: list[IntersectionAnimationCarDescription] = [
    {
        "registry_number": "DW001",
        "color": PRIMARY_CAR_COLOR,
        "manoeuvre_description": {
            "starting_side": CardinalDirection.LEFT,
            "ending_side": CardinalDirection.DOWN,
        },
        "model": TOYOTA_YARIS_SPECIFICATION,
        "start_frame_number": 0,
        "velocity": 0,
    },
    {
        "registry_number": "DW002",
        "color": SECONDARY_CAR_COLOR,
        "manoeuvre_description": {
            "starting_side": CardinalDirection.UP,
            "ending_side": CardinalDirection.DOWN,
        },
        "model": TOYOTA_YARIS_SPECIFICATION,
        "start_frame_number": 0,
        "velocity": 3,
    },
    {
        "registry_number": "DW003",
        "color": SECONDARY_CAR_COLOR,
        "manoeuvre_description": {
            "starting_side": CardinalDirection.DOWN,
            "ending_side": CardinalDirection.LEFT,
        },
        "model": TOYOTA_YARIS_SPECIFICATION,
        "start_frame_number": 0,
        "velocity": 0,
    },
    {
        "registry_number": "DW004",
        "color": SECONDARY_CAR_COLOR,
        "manoeuvre_description": {
            "starting_side": CardinalDirection.RIGHT,
            "ending_side": CardinalDirection.DOWN,
        },
        "model": TOYOTA_YARIS_SPECIFICATION,
        "start_frame_number": 0,
        "velocity": 3,
    },
]


class IntersectionI3TurnRightAnimation(IntersectionI3Animation):
    def __init__(self, *, previous_app_screen: ApplicationScreen | None = None):
        super().__init__(
            CARS_DESCRIPTIONS,
            MANOEUVRE_CONTROL_INSTRUCTIONS_DIR_NAME,
            previous_app_screen=previous_app_screen,
        )
