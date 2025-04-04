from abc import ABC, abstractmethod
from enum import Enum
from car.model import CarModel
from smart_city.road_control_center.manoeuvres.track import TrackPath


class TrackSegmentType(Enum):
    STRAIGHT_PATH = "STRAIGHT_PATH"
    TURN = "TURN"


class TrackSegment(ABC):
    def __init__(
        self,
        type: TrackSegmentType,
        track_path: TrackPath,
    ) -> None:
        self.type = type
        self.track_path = track_path

    @abstractmethod
    def get_max_safe_velocity(self, car_model: CarModel) -> float:
        raise NotImplementedError
