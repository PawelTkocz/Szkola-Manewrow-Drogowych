from abc import ABC, abstractmethod
from typing import TypedDict
from car.autonomous.track import TrackPath
from car.car import CarState, SpeedModifications
from geometry import Directions


class MovementDecision(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions


class TrackFollower(ABC):
    @abstractmethod
    def set_track(self, track_path: TrackPath) -> None:
        pass

    @abstractmethod
    def make_movement_decision(self, car_state: CarState) -> MovementDecision:
        pass
