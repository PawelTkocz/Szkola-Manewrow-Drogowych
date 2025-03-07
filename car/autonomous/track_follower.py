from abc import ABC, abstractmethod
from typing import TypedDict
from car.autonomous.track import TrackPath
from car.car import LiveCarData, SpeedModifications
from geometry import Directions
from manoeuvres.manoeuvre_phase import ManoeuvrePhaseEndState


class MovementDecision(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions


class TrackFollower(ABC):
    @abstractmethod
    def set_track(self, track_path: TrackPath) -> None:
        pass

    @abstractmethod
    def make_movement_decision(self, live_car_data: LiveCarData, desired_end_state: ManoeuvrePhaseEndState) -> MovementDecision:
        pass
