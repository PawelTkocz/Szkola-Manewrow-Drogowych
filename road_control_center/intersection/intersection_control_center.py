from abc import abstractmethod
from car.autonomous_car import CarDataTransmitter
from geometry import Directions
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from road_control_center.intersection.intersection_control_center_software import (
    can_cross_intersection_without_priority_violation,
)
from road_control_center.intersection.schemas import (
    CarOnIntersection,
    IntersectionManoeuvreDescription,
)
from road_control_center.road_control_center import RoadControlCenter
from road_segments.intersection.intersection import Intersection
from traffic_control_center_software.car_movement_simulator import (
    can_stop_before_zone,
    get_status_before_entering_zone,
)

from traffic_control_center_software.schemas import (
    MovementInstruction,
    SpeedModifications,
)
from traffic_control_center_software.track_follower import TrackFollower


class IntersectionControlCenter(RoadControlCenter):
    def __init__(self, intersection: Intersection):
        super().__init__()
        self.intersection = intersection
        self.cars: list[CarOnIntersection] = []
        self.track_follower = TrackFollower()

    def add_car(self, car_data_transmitter: CarDataTransmitter):
        live_car_data = car_data_transmitter.get_live_car_data()
        manoeuvre_description = live_car_data["manoeuvres"][self.intersection.id]
        starting_side = manoeuvre_description["starting_side"]
        ending_side = manoeuvre_description["ending_side"]
        manoeuvre = IntersectionManoeuvre(
            live_car_data["model"], self.intersection, starting_side, ending_side
        )
        self.cars.append(
            {
                "car_data_transmitter": car_data_transmitter,
                "manoeuvre": manoeuvre,
                "manoeuvre_status": {"can_safely_cross_intersection": False},
            }
        )

    def remove_car(self, car_data_transmitter: CarDataTransmitter):
        self.cars = [
            car
            for car in self.cars
            if car["car_data_transmitter"] != car_data_transmitter
        ]

    def get_car_movement_instruction(
        self, car: CarOnIntersection
    ) -> MovementInstruction:
        live_car_data = car["car_data_transmitter"].get_live_car_data()
        manoeuvre = car["manoeuvre"]
        manoeuvre_status = car["manoeuvre_status"]
        if manoeuvre_status["can_safely_cross_intersection"]:
            desired_end_state = manoeuvre.phases[0].desired_end_state
            track = manoeuvre.phases[0].track
            return self.track_follower.get_movement_instruction(
                live_car_data, track, desired_end_state
            )

        # we know that the car still didn't enter the intersection
        speed_modifications = [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]
        for speed_modification in speed_modifications:
            if can_stop_before_zone(
                live_car_data,
                manoeuvre.phases[0].track,
                self.intersection.intersection_parts["intersection_area"],
            ):
                return speed_modification

            return speed_modification

        return SpeedModifications.BRAKE

    @abstractmethod
    def can_enter_intersection(
        self, intersection_side: Directions, car_velocity: float, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign and so on)"""
        pass

    @abstractmethod
    def has_priority(
        car1_manoeurve_description: IntersectionManoeuvreDescription,
        car2_manoeuvre_description: IntersectionManoeuvreDescription,
        time: int,
    ) -> bool:
        pass

    def get_cars_with_priority(
        self, car: CarOnIntersection, time: int
    ) -> list[CarOnIntersection]:
        return [
            intersection_car
            for intersection_car in self.cars
            if intersection_car is not car
            and self.has_priority(
                intersection_car["manoeuvre_description"],
                car["manoeuvre_description"],
                time,
            )
        ]

    def can_cross_the_intersection(self, car: CarOnIntersection) -> bool:
        live_car_data = car["car_data_transmitter"].get_live_car_data()
        track = car["manoeuvre"].phases[0].track
        entering_intersection_status = get_status_before_entering_zone(
            live_car_data,
            track,
            self.intersection.intersection_parts["intersection_area"],
        )
        time_to_enter_intersection = entering_intersection_status["time_to_enter_zone"]
        entering_intersection_live_car_data = entering_intersection_status[
            "live_car_data"
        ]
        if not self.can_enter_intersection(
            car["manoeuvre_description"]["starting_side"],
            entering_intersection_live_car_data["velocity"],
            self._time + time_to_enter_intersection,
        ):
            return False

        cars_with_priority = self.get_cars_with_priority(
            car, self._time + time_to_enter_intersection
        )
        return can_cross_intersection_without_priority_violation(
            car, cars_with_priority
        )
