# in the future road_control_center can be list of centers, and after each frame
# the traffic control center should reassign car to road control centers based on
# car position.

from car.car import Car
from car.instruction_controlled_car import InstructionControlledCar
from car.model import CarModel
from geometry import Direction, Directions, Point
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription
from road_control_center.road_control_center import RoadControlCenter
from traffic_control_center.schemas import LiveCarData
from traffic_control_center_software.schemas import (
    MovementInstruction,
)


class TrafficControlCenter:
    def __init__(self, road_control_center: RoadControlCenter):
        self._road_control_center = road_control_center
        self._time = 0

    def receive_live_car_data(self, live_car_data: LiveCarData):
        pass

    def send_movement_instruction(self, registry_number: str) -> MovementInstruction:
        pass

    def tick(self):
        self._time += 1
        self._road_control_center.update_time()


class CarDataTransmitter:
    def __init__(self, autonomous_car: "SmartTrafficCar"):
        self._autonomous_car = autonomous_car
        self._traffic_control_center: TrafficControlCenter | None = None

    def connect_to_traffic_control_center(
        self, traffic_control_center: TrafficControlCenter
    ):
        self._traffic_control_center = traffic_control_center
        self.send_live_data_to_control_center()

    def send_live_data_to_control_center(self):
        if self._traffic_control_center:
            self._traffic_control_center.receive_live_car_data(
                self._autonomous_car.get_live_data()
            )

    def fetch_movement_instruction(self) -> MovementInstruction | None:
        return (
            self._traffic_control_center.send_movement_instruction(
                self._autonomous_car.registry_number
            )
            if self._traffic_control_center
            else None
        )


class SmartTrafficCar(InstructionControlledCar):
    def __init__(
        self,
        manoeuvre_description: IntersectionManoeuvreDescription,
        registry_number: str,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        super().__init__(
            registry_number, model, color, front_middle_position, direction, velocity
        )
        self.car_data_transmitter = CarDataTransmitter(self)
        self.manoeuvre_description = manoeuvre_description

    def tick(self) -> MovementInstruction | None:
        movement_instruction = self.car_data_transmitter.fetch_movement_instruction()
        if movement_instruction:
            self.apply_movement_instruction(movement_instruction)
        self.move()
        self.car_data_transmitter.send_live_data_to_control_center()
        return movement_instruction

    def connect_to_traffic_control_center(
        self, traffic_control_center: TrafficControlCenter
    ):
        self.car_data_transmitter.connect_to_traffic_control_center(
            traffic_control_center
        )

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
            "registry_number": self.registry_number,
            "manoeuvre_description": self.manoeuvre_description,
        }
