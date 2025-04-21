from abc import ABC, abstractmethod

from schemas import CardinalDirection
from smart_city.road_control_center.intersection.schemas import (
    IntersectionPriorityCarInfo,
)
from utils import clockwise_direction_shift


class IntersectionRules(ABC):
    def has_emergency_priority(
        self,
        car1_info: IntersectionPriorityCarInfo,
        car2_info: IntersectionPriorityCarInfo,
    ):
        if car1_info["high_priority"] and not car2_info["high_priority"]:
            return True

    def intersection_sides_passed_on_right(
        self, starting_side: CardinalDirection, ending_side: CardinalDirection
    ) -> list[CardinalDirection]:
        sides_passed_on_right = []
        for i in range(1, 4):
            direction = clockwise_direction_shift(ending_side, i)
            if direction != starting_side:
                sides_passed_on_right.append(direction)
            else:
                break
        return sides_passed_on_right

    def tracks_intersect(
        self,
        car1_info: IntersectionPriorityCarInfo,
        car2_info: IntersectionPriorityCarInfo,
    ) -> bool:
        car1_sides_passed_on_right = self.intersection_sides_passed_on_right(
            car1_info["manoeuvre_description"]["starting_side"],
            car1_info["manoeuvre_description"]["ending_side"],
        )
        car2_sides_passed_on_right = self.intersection_sides_passed_on_right(
            car2_info["manoeuvre_description"]["starting_side"],
            car2_info["manoeuvre_description"]["ending_side"],
        )
        return (
            car1_info["manoeuvre_description"]["starting_side"]
            in car2_sides_passed_on_right
            or car1_info["manoeuvre_description"]["ending_side"]
            in car2_sides_passed_on_right
            or car2_info["manoeuvre_description"]["starting_side"]
            in car1_sides_passed_on_right
            or car2_info["manoeuvre_description"]["ending_side"]
            in car1_sides_passed_on_right
        )

    @abstractmethod
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign, ambulance and so on)"""
        raise NotImplementedError

    @abstractmethod
    def is_on_road_with_priority(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        raise NotImplementedError

    def must_yield_the_right_of_way(
        self,
        car1_info: IntersectionPriorityCarInfo,
        car2_info: IntersectionPriorityCarInfo,
        time: int,
    ) -> bool:
        if not self.tracks_intersect(car1_info, car2_info):
            return False
        if self.has_emergency_priority(car2_info, car1_info):
            return True
        if self.has_emergency_priority(car1_info, car2_info):
            return False
        car1_priority_road = self.is_on_road_with_priority(car1_info, time)
        car2_priority_road = self.is_on_road_with_priority(car2_info, time)
        if car1_priority_road and not car2_priority_road:
            return False
        if car2_priority_road and not car1_priority_road:
            return True
        return car2_info["manoeuvre_description"][
            "starting_side"
        ] in self.intersection_sides_passed_on_right(
            car1_info["manoeuvre_description"]["starting_side"],
            car1_info["manoeuvre_description"]["ending_side"],
        )
