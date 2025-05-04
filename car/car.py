from car.car_body import CarBody
from car.car_lights import CarLights
from car.chassis.chassis import Chassis
from car.schemas import AccelerationDirection, CarColors
from car.model import CarModelSpecification
from car.turn_signals import TurnSignalType
from geometry.direction import Direction
from geometry.shapes.rectangle import Rectangle
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
from schemas import HorizontalDirection


DEFAULT_CAR_COLORS: CarColors = {
    "body": {"shell": "#ff0000", "side_mirrors": "#000000", "windows": "#000000"},
    "chassis": {"chassis": "#000000", "wheels": "#262626"},
    "lights": {"default": "#ffc100", "turn_signal": "#ff6500"},
}


class Car:
    def __init__(
        self,
        registry_number: str,
        model_specification: CarModelSpecification,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        wheels_angle: float = 0,
        colors: CarColors = DEFAULT_CAR_COLORS,
        *,
        shell_color: str | None = None,
    ):
        self.chassis = Chassis(
            model_specification["chassis"],
            colors["chassis"],
            model_specification["steering_system"],
            model_specification["wheels"],
            wheels_angle,
            front_middle_position,
            direction,
        )
        self.specification = model_specification
        self.registry_number = registry_number
        self.velocity = velocity
        self.lights = CarLights(
            model_specification["lights"],
            colors["lights"],
            front_middle_position,
            direction,
        )
        self.colors = colors
        if shell_color:
            self.colors["body"]["shell"] = shell_color

        self.body = CarBody(
            [self.lights.left_light, self.lights.right_light],
            model_specification["body"],
            colors["body"],
            front_middle_position,
            direction,
        )

    def turn(self, direction: HorizontalDirection) -> None:
        self.chassis.turn(direction)

    def accelerate(self, direction: AccelerationDirection) -> None:
        max_velocity = self.specification["motion"]["max_velocity"]
        acceleration = self.specification["motion"]["acceleration"]
        if direction == AccelerationDirection.FORWARD:
            self.velocity = min(self.velocity + acceleration, max_velocity)
        elif direction == AccelerationDirection.REVERSE:
            self.velocity = max(self.velocity - acceleration, -1 * max_velocity)

    def _slow_down(self, velocity_decrease: float) -> None:
        self.velocity = (
            max(self.velocity - velocity_decrease, 0)
            if self.velocity > 0
            else min(self.velocity + velocity_decrease, 0)
        )

    def brake(self) -> None:
        self._slow_down(self.specification["motion"]["brake_force"])

    def activate_turn_signal(self, side: HorizontalDirection) -> None:
        self.lights.activate_turn_signal(side)

    def deactivate_turn_signal(self) -> None:
        self.lights.deactivate_turn_signal()

    @property
    def width(self) -> float:
        return self.chassis.width

    @property
    def length(self) -> float:
        return self.chassis.length

    @property
    def direction(self) -> Direction:
        return self.chassis.direction

    @property
    def front_middle(self) -> Point:
        return self.chassis.front_middle

    @property
    def wheels_angle(self) -> float:
        return self.chassis.wheels_angle

    @property
    def turn_signal(self) -> TurnSignalType:
        return self.lights.turn_signal

    @property
    def acceleration(self) -> float:
        return self.specification["motion"]["acceleration"]

    @property
    def max_velocity(self) -> float:
        return self.specification["motion"]["max_velocity"]

    def collides(self, obj: Rectangle) -> bool:
        return self.chassis.collides(obj)

    def is_point_inside(self, point: Point) -> bool:
        return self.chassis.is_point_inside(point)

    def move(self) -> None:
        if self.velocity == 0:
            return
        self.chassis.move(self.velocity)
        self._slow_down(self.specification["motion"]["rolling_resistance"])
        self.body.update_position(self.front_middle, self.direction)

    def draw(self, road_elements_drafter: RoadElementsDrafter) -> None:
        self.chassis.draw_on_road(road_elements_drafter)
        self.body.draw_on_road(road_elements_drafter)

    def tick(self) -> None:
        self.move()
        self.lights.tick()
