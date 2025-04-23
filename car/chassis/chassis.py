from pygame import Surface
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
from car.schemas import ChassisColoristics
from geometry.direction import Direction
from geometry.shapes.rectangle import DynamicRectangle
from geometry.vector import Point, Vector
from schemas import HorizontalDirection


class Chassis(DynamicRectangle):
    def __init__(
        self,
        specification: ChassisSpecification,
        coloristics: ChassisColoristics,
        steering_system_specification: SteeringSystemSpecification,
        wheel_specification: WheelsSpecification,
        wheels_angle: float,
        front_middle: Point,
        direction: Direction,
    ):
        super().__init__(
            front_middle,
            specification["width"],
            specification["length"],
            direction,
            coloristics["chassis"],
        )
        self.steering_system = SteeringSystem(
            steering_system_specification, wheels_angle
        )
        wheels_positions = self._get_wheels_positions(
            wheel_specification["width"], wheel_specification["length"]
        )
        self.left_wheel = Wheel(
            wheels_positions["left"]["corners"],
            wheels_positions["left"]["middle"],
            coloristics["wheels"],
            self.front_middle,
            self.direction,
        )
        self.right_wheel = Wheel(
            wheels_positions["right"]["corners"],
            wheels_positions["right"]["middle"],
            coloristics["wheels"],
            self.front_middle,
            self.direction,
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
        }

    @property
    def wheels_angle(self) -> float:
        return self.steering_system.wheels_angle

    def move(self, distance: float) -> None:
        movement_vector = self.steering_system.get_wheels_direction(
            self.direction
        ).scale_to_len(distance)

        # this should not come from front_middle
        new_front_middle = self.front_middle.add_vector(movement_vector)
        length_vector = Vector(new_front_middle, self.rear_middle).scale_to_len(
            self.length
        )
        new_rear_middle = new_front_middle.copy().add_vector(
            length_vector.get_negative_of_a_vector()
        )
        new_direction = Direction(new_front_middle, new_rear_middle)
        self.update_position(new_front_middle, new_direction)
        self._update_wheels_positions()

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

    def draw(
        self,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        self.left_wheel.draw(
            screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        )
        self.right_wheel.draw(
            screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        )
        super().draw(screen, scale_factor=scale_factor, screen_y_offset=screen_y_offset)
