from animations.animations_generators.constants import PRIMARY_CAR_COLOR
from animations.animations_generators.intersection_I2.intersection_I2_animations import (
    IntersectionI2Animation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from car.toyota_yaris_specification import TOYOTA_YARIS_SPECIFICATION
from schemas import CardinalDirection

MANOEUVRE_CONTROL_INSTRUCTIONS_DIR_NAME = "go_straight"
CARS_DESCRIPTIONS: list[IntersectionAnimationCarDescription] = [
    {
        "registry_number": "DW001",
        "color": PRIMARY_CAR_COLOR,
        "manoeuvre_description": {
            "starting_side": CardinalDirection.LEFT,
            "ending_side": CardinalDirection.RIGHT,
        },
        "model": TOYOTA_YARIS_SPECIFICATION,
        "start_frame_number": 0,
        "velocity": 2,
    },
]


class IntersectionI2GoStraightAnimation(IntersectionI2Animation):
    def __init__(self, *, previous_app_screen: ApplicationScreen | None = None):
        super().__init__(
            CARS_DESCRIPTIONS,
            MANOEUVRE_CONTROL_INSTRUCTIONS_DIR_NAME,
            previous_app_screen=previous_app_screen,
        )
