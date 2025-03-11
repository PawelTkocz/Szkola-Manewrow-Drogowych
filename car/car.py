from enum import Enum
from typing import TypeAlias
from car.schemas import LiveCarData
from geometry import Direction, Directions, Point, Rectangle, Vector
from car.model import CarModel
from car.wheels import Wheels
from drafter.car import CarDrafter
from intersection.intersection import Intersection

RoadSegment: TypeAlias = Intersection


class SpeedModifications(Enum):
    SPEED_UP = 1
    NO_CHANGE = 2
    BRAKE = 3


class CarBody(Rectangle):
    def __init__(
        self, front_middle: Point, width: float, length: float, direction: Direction
    ):
        super().__init__(front_middle, width, length, direction)

    def move(self, direction: Directions, front_vector: Vector):
        if direction == Directions.RIGHT:
            self.move_left_side(front_vector)
        else:
            self.move_right_side(front_vector)
        # czemu zmiana z left na right i odwrotnie rozwiazuje problem z tym, ze jadac prosto
        # zblizalismy sie wolniej do celu niz skrecajac

    # think about unifying this to just move - vector from front middle
    def move_left_side(self, front_vector: Vector):
        new_front_left = self.front_left.add_vector(front_vector)
        length_vector = Vector(new_front_left, self.rear_left).scale_to_len(self.length)
        new_rear_left = new_front_left.copy().add_vector(
            length_vector.get_negative_of_a_vector()
        )
        new_direction = Direction(new_front_left, new_rear_left)
        new_front_middle = new_front_left.copy().add_vector(
            length_vector.get_orthogonal_vector(Directions.RIGHT, self.width / 2)
        )
        self.update_position(new_front_middle, new_direction)

    def move_right_side(self, front_vector: Vector):
        new_front_right = self.front_right.add_vector(front_vector)
        length_vector = Vector(new_front_right, self.rear_right).scale_to_len(
            self.length
        )
        new_rear_right = new_front_right.copy().add_vector(
            length_vector.get_negative_of_a_vector()
        )
        new_direction = Direction(new_front_right, new_rear_right)
        new_front_middle = new_front_right.copy().add_vector(
            length_vector.get_orthogonal_vector(Directions.LEFT, self.width / 2)
        )
        self.update_position(new_front_middle, new_direction)


class Car(CarBody):
    """
    Class representing a car in Cartesian coordinate system.
    """

    def __init__(
        self,
        registry_number: int,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        road_segment: RoadSegment,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        """
        Initialize car
        """
        super().__init__(front_middle_position, model.width, model.length, direction)
        self.registry_number = registry_number
        self.model = model
        self.color = color
        self.velocity = velocity
        self.wheels = Wheels(model.max_wheels_turn)
        self._road_segment = road_segment
        self._car_drafter = CarDrafter(model, color)

    @property
    def wheels_angle(self) -> float:
        return self.wheels.angle

    @property
    def turn_direction(self) -> Directions:
        return self.wheels.current_direction

    @property
    def max_acceleration(self) -> float:
        return self.model.max_acceleration

    @property
    def max_velocity(self) -> float:
        return self.model.max_velocity

    @property
    def max_brake(self) -> float:
        return self.model.max_brake

    @property
    def wheels_turn_speed(self) -> float:
        return self.model.wheels_turn_speed

    @property
    def wheels_direction(self) -> Direction:
        return self.wheels.direction

    @property
    def current_road_segment(self) -> RoadSegment:
        return self._road_segment


    def turn(self, direction: Directions):
        self.wheels.turn(self.wheels_turn_speed, direction)

    def speed_up(self, direction: Directions, limit=None):
        if (self.velocity > 0 and direction == Directions.BACK) or (
            self.velocity < 0 and direction == Directions.FRONT
        ):
            return
        if limit is not None and abs(self.velocity) > limit:
            self.brake()
            return
        if direction == Directions.FRONT:
            self.velocity = min(
                self.velocity + self.max_acceleration,
                self.max_velocity,
                limit if limit is not None else self.max_velocity,
            )
        elif direction == Directions.BACK:
            self.velocity = max(
                self.velocity - self.max_acceleration,
                -1 * self.max_velocity,
                limit if limit is not None else -1 * self.max_velocity,
            )

    def slow_down(self, value):
        self.velocity = (
            max(self.velocity - value, 0)
            if self.velocity > 0
            else min(self.velocity + value, 0)
        )

    def brake(self):
        self.slow_down(self.max_brake)

    def move(self):
        if self.velocity == 0:
            return

        front_movement_vector = self.direction.turn(self.wheels_angle).scale_to_len(
            self.velocity
        )
        super().move(self.turn_direction, front_movement_vector)
        self.slow_down(self.model.resistance)

    def draw(self, screen):
        self._car_drafter.draw(self, self.wheels_angle, screen)

    def collides(self, obj: Rectangle):
        if obj is not None:
            return self.collides(obj)
        return False
    
    def get_live_data(self) -> LiveCarData:
        return {
            "length": self.length,
            "width": self.width,
            "direction": self.direction,
            "front_middle": self.front_middle,
            "front_right": self.front_right,
            "front_left": self.front_left,
            "rear_middle": self.rear_middle,
            "rear_left": self.rear_left,
            "rear_right": self.rear_right,
            "color": self.color,
            "model": self.model,
            "wheels_angle": self.wheels_angle,
            "max_acceleration": self.max_acceleration,
            "velocity": self.velocity,
            "max_velocity": self.max_velocity,
            "max_brake": self.max_brake,
            "road_segment": self.current_road_segment,
            "autonomous_driving_program": None,
            "registry_number": self.registry_number,
            "current_manoeuvre": None
        }
    
    def update_current_road_segment(self, road_segment: Intersection):
        """
        Update current road segment the car is on.
        """
        self.current_road_segment = road_segment
