from car.car_part import CarPart
from car.model import BodySpecification
from car.schemas import CarBodyColors
from geometry.direction import Direction
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter


class CarBody:
    def __init__(
        self,
        lights: list[CarPart],
        specification: BodySpecification,
        colors: CarBodyColors,
        car_front_middle: Point,
        car_direction: Direction,
    ) -> None:
        self.lights = lights
        self.shell = CarPart(
            specification["shell"],
            colors["shell"],
            car_front_middle,
            car_direction,
        )
        self.side_mirrors = [
            CarPart(position, colors["side_mirrors"], car_front_middle, car_direction)
            for position in (
                specification["left_side_mirror"],
                specification["right_side_mirror"],
            )
        ]
        self.windows = [
            CarPart(position, colors["windows"], car_front_middle, car_direction)
            for position in (
                specification["front_window"],
                specification["left_window"],
                specification["right_window"],
                specification["rear_window"],
            )
        ]
        self.body_parts = [self.shell] + self.side_mirrors + self.windows + self.lights

    def update_position(
        self, car_front_middle: Point, car_direction: Direction
    ) -> None:
        for part in self.body_parts:
            part.update_position(car_front_middle, car_direction)

    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        for part in self.body_parts:
            road_elements_drafter.draw_polygon(part)
