from abc import ABC, abstractmethod

from road_control_center.intersection.schemas import IntersectionPriorityCarInfo


class IntersectionRules(ABC):
    @abstractmethod
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign, ambulance and so on)"""
        raise NotImplementedError

    @abstractmethod
    def has_priority(
        car1_info: IntersectionPriorityCarInfo,
        car2_info: IntersectionPriorityCarInfo,
        time: int,
    ) -> bool:
        """Determine if car1 has priority over car2 in specified moment."""
        raise NotImplementedError
