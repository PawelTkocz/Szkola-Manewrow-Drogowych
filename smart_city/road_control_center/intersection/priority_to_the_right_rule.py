from geometry import Directions
from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
    IntersectionPriorityCarInfo,
)


class PriorityToTheRightRule(IntersectionRules):
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign)"""
        # there are no stop signs, no traffic lights
        return True

    def has_priority(
        self,
        car1_info: IntersectionPriorityCarInfo,
        car2_info: IntersectionPriorityCarInfo,
        time: int,
    ) -> bool:
        if car1_info["high_priority"] and not car2_info["high_priority"]:
            return True
        if not car1_info["high_priority"] and car2_info["high_priority"]:
            return False
        sides = [Directions.DOWN, Directions.RIGHT, Directions.UP, Directions.LEFT]
        car1_starting_side = car1_info["manoeuvre_description"]["starting_side"]
        car1_ending_side = car1_info["manoeuvre_description"]["ending_side"]
        car2_starting_side = car2_info["manoeuvre_description"]["starting_side"]
        car1_starting_side_index = sides.index(car1_starting_side)
        side_index = (car1_starting_side_index + 1) % 4
        while sides[side_index] != car1_ending_side:
            if sides[side_index] == car2_starting_side:
                return False
            side_index = (side_index + 1) % 4
        return True
