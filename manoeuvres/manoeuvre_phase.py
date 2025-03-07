from abc import ABC, abstractmethod
from typing import TypedDict
from car.autonomous.track import Track, TrackPath
from geometry import Point

class ManoeuvrePhaseEndState(TypedDict):
    front_middle_position: Point
    velocity: float

class ManoeuvrePhase(ABC):
    """
    Class representing one phase of a manoeuvre.
    """

    def __init__(self, track_path: TrackPath, reversing: bool):
        self.track = Track(track_path)
        self.reversing = reversing

    @abstractmethod
    def get_desired_end_state() -> ManoeuvrePhaseEndState:
        pass

    @abstractmethod
    def is_phase_over(self, front_middle_position: Point, velocity: float) -> bool:
        pass
