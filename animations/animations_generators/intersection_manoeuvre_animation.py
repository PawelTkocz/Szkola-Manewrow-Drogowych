import os

from animations.animations_generators.road_segment_animation import RoadSegmentAnimation
from animations.animations_generators.schemas import (
    AnimationCarDescription,
    CarStartingPosition,
    IntersectionAnimationCarDescription,
)
from application_screen import ApplicationScreen
from geometry.direction import Direction
from geometry.vector import Point
from road_segments.intersection.intersection import Intersection
from animations.animations_generators.constants import (
    CONTROL_INSTRUCTIONS_DIR as CONTROL_INSTRUCTIONS_DIR,
)
from smart_city.schemas import IntersectionManoeuvreDescription
from smart_city.traffic_control_center import TrafficControlCenter


class IntersectionManoeuvreAnimation(RoadSegmentAnimation):
    def __init__(
        self,
        intersection: Intersection,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        traffic_control_center: TrafficControlCenter,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ):
        self.intersection = intersection
        control_instructions_dir_path = os.path.join(
            CONTROL_INSTRUCTIONS_DIR,
            traffic_control_center._road_control_center.id,
            manoeuvre_control_instructions_dir_name,
        )
        animation_cars_descriptions: list[AnimationCarDescription] = [
            {
                "model": car_description["model"],
                "color": car_description["color"],
                "registry_number": car_description["registry_number"],
                "velocity": car_description["velocity"],
                "start_frame_number": car_description["start_frame_number"],
                "manoeuvre_description": car_description["manoeuvre_description"],
                "starting_position": self.get_starting_position(
                    car_description["manoeuvre_description"]
                ),
            }
            for car_description in cars_descriptions
        ]
        super().__init__(
            intersection,
            animation_cars_descriptions,
            control_instructions_dir_path,
            traffic_control_center,
            previous_app_screen=previous_app_screen,
        )

    def get_starting_position(
        self, manoeuvre_description: IntersectionManoeuvreDescription
    ) -> CarStartingPosition:
        starting_side = manoeuvre_description["starting_side"]
        front_middle_position = self.intersection.intersection_parts["incoming_lanes"][
            starting_side
        ].rear_middle
        direction = self.intersection.intersection_parts["incoming_lanes"][
            starting_side
        ].direction
        return {
            "front_middle": front_middle_position,
            "direction": direction,
            "wheels_angle": 0,
        }
