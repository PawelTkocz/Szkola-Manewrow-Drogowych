import math
from Geometry import Direction, Directions, Point, Rectangle, Vector
from cars.Brand import Brand
from cars.Wheels import Wheels


class Car:
    """
    Class representing a car in Cartesian coordinate system
    """

    def __init__(
        self,
        brand: Brand,
        front_left_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        """
        Initialize car
        """
        self.brand = brand
        self.velocity = velocity
        self.body = Rectangle(front_left_position, brand.width, brand.length, direction)
        self.wheels = Wheels(self.brand.max_wheels_turn)

    @property
    def direction(self) -> Direction:
        return self.body.direction

    @property
    def front_left(self) -> Point:
        return self.body.front_left

    @property
    def front_right(self) -> Point:
        return self.body.front_right

    @property
    def rear_left(self) -> Point:
        return self.body.rear_left

    @property
    def rear_right(self) -> Point:
        return self.body.rear_right

    @property
    def wheels_angle(self) -> float:
        return self.wheels.angle

    @property
    def turn_direction(self) -> Directions:
        return self.wheels.current_direction

    @property
    def length(self) -> float:
        return self.brand.length

    @property
    def width(self) -> float:
        return self.brand.width

    @property
    def max_acceleration(self) -> float:
        return self.brand.max_acceleration

    @property
    def max_velocity(self) -> float:
        return self.brand.max_velocity

    @property
    def max_brake(self) -> float:
        return self.brand.max_brake

    def turn(self, direction: Directions):
        self.wheels.turn(self.brand.wheels_turn_speed, direction)

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

    def _calculate_rear_movement_vector2(self, front_movement_vector: Vector):
        """ """
        # dziala calkiem dobrze nawet dla 10000
        return Vector(Point(0, 0))

    def _calculate_rear_movement_vector(self, front_movement_vector: Vector):
        """ """
        # jesli bedzie za dlugo liczylo sprobowac wrocic do starej wersji
        # dla 1000 wykonan wydoczne lagowanie, dla 2000 dziala bardzo wolno
        front_corner_final_position = self.front_left.add_vector(front_movement_vector)
        rear_corner_start_position = self.rear_left
        x1, y1 = rear_corner_start_position.x, rear_corner_start_position.y
        x2, y2 = self.direction.x, self.direction.y
        x3, y3 = front_corner_final_position.x, front_corner_final_position.y
        delta_a = x2**2 + y2**2
        delta_b = 2 * (x1 * x2 + y1 * y2 - x2 * x3 - y2 * y3)
        delta_c = (
            x1**2 + y1**2 + x3**2 + y3**2 - 2 * (x1 * x3 + y1 * y3) - self.length**2
        )
        delta = delta_b**2 - 4 * delta_a * delta_c
        if delta < 0:
            return Vector(Point(0, 0))
        res1 = (-delta_b - math.sqrt(delta)) / (2 * delta_a)
        res2 = (math.sqrt(delta) - delta_b) / (2 * delta_a)
        return self.direction.scale(min(res1, res2))

    def move(self):
        if self.velocity == 0:
            return

        front_movement_vector = self.direction.turn(self.wheels_angle).scale_to_len(
            self.velocity
        )
        rear_movement_vec = self._calculate_rear_movement_vector2(front_movement_vector)
        if self.turn_direction == Directions.RIGHT:
            self.body.move_right_side(front_movement_vector, rear_movement_vec)
        else:
            self.body.move_left_side(front_movement_vector, rear_movement_vec)
        self.slow_down(self.brand.resistance)

    def draw(self, screen):
        self.brand.draw(self.body, self.wheels_angle, screen)

    def collides(self, obj):
        pass
