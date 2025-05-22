from car.car_part import get_car_point_position
from car.chassis.schemas import (
    WheelsPositions,
)
from car.chassis.steering_system import SteeringSystem
from car.chassis.wheel import Wheel
from car.model import (
    ChassisSpecification,
    SteeringSystemSpecification,
    WheelsSpecification,
)
from car.schemas import ChassisColors
from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
from schemas import HorizontalDirection


class Chassis(DynamicRectangle):
    def __init__(
        self,
        specification: ChassisSpecification,
        colors: ChassisColors,
        steering_system_specification: SteeringSystemSpecification,
        wheels_specification: WheelsSpecification,
        wheels_angle: float,
        front_middle: Point,
        direction: Direction,
    ):
        super().__init__(
            front_middle,
            specification["width"],
            specification["length"],
            direction,
            colors["chassis"],
        )
        self.steering_system = SteeringSystem(
            steering_system_specification, wheels_angle
        )
        wheels_positions = self._get_wheels_positions(
            wheels_specification["width"], wheels_specification["length"]
        )
        self.left_wheel = Wheel(
            wheels_positions["left"]["corners"],
            wheels_positions["left"]["middle"],
            colors["wheels"],
            self.front_middle,
            self.direction,
        )
        self.right_wheel = Wheel(
            wheels_positions["right"]["corners"],
            wheels_positions["right"]["middle"],
            colors["wheels"],
            self.front_middle,
            self.direction,
        )
        self.relative_axle_center_position = wheels_positions["axle_center"]
        self._axle_center = get_car_point_position(
            self.front_middle, self.direction, self.relative_axle_center_position
        )

    def _get_wheels_positions(
        self, wheels_width: float, wheels_length: float
    ) -> WheelsPositions:
        car_width = self.width
        return {
            "left": {
                "middle": {
                    "x": -1 * (car_width / 2 - wheels_width / 2),
                    "y": -0.5 * wheels_length,
                },
                "corners": [
                    {"x": -1 * car_width / 2, "y": 0},
                    {"x": -1 * (car_width / 2 - wheels_width), "y": 0},
                    {"x": -1 * (car_width / 2 - wheels_width), "y": -1 * wheels_length},
                    {"x": -1 * car_width / 2, "y": -1 * wheels_length},
                ],
            },
            "right": {
                "middle": {
                    "x": car_width / 2 - wheels_width / 2,
                    "y": -0.5 * wheels_length,
                },
                "corners": [
                    {"x": car_width / 2 - wheels_width, "y": 0},
                    {"x": car_width / 2, "y": 0},
                    {"x": car_width / 2, "y": -1 * wheels_length},
                    {"x": car_width / 2 - wheels_width, "y": -1 * wheels_length},
                ],
            },
            "axle_center": {"x": 0, "y": -0.5 * wheels_length},
        }

    @property
    def wheels_angle(self) -> float:
        return self.steering_system.wheels_angle

    @property
    def axle_center(self) -> Point:
        return self._axle_center.copy()

    def move(self, distance: float) -> None:
        movement_vector = self.steering_system.get_wheels_direction(
            self.direction
        ).scale_to_len(distance)

        new_axle_center = self.axle_center.add_vector(movement_vector)
        new_direction = Direction(new_axle_center, self.rear_middle)
        new_rear_middle = new_axle_center.copy().add_vector(
            new_direction.get_negative_of_a_vector().scale_to_len(
                self.axle_center.distance(self.rear_middle)
            )
        )
        new_front_middle = new_rear_middle.add_vector(
            new_direction.copy().scale_to_len(self.length)
        )
        self.update_position(new_front_middle, new_direction)
        self._update_wheels_positions()
        self._axle_center = get_car_point_position(
            self.front_middle, self.direction, self.relative_axle_center_position
        )

    def turn(self, direction: HorizontalDirection) -> None:
        self.steering_system.turn(direction)
        self._update_wheels_positions()

    def _update_wheels_positions(self) -> None:
        self.left_wheel.update_position(
            self.front_middle, self.direction, self.steering_system.wheels_angle
        )
        self.right_wheel.update_position(
            self.front_middle, self.direction, self.steering_system.wheels_angle
        )

    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        road_elements_drafter.draw_polygon(self.left_wheel)
        road_elements_drafter.draw_polygon(self.right_wheel)
        road_elements_drafter.draw_polygon(self)
