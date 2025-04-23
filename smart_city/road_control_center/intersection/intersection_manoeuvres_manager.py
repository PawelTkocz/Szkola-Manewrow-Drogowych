from enum import Enum
import json
import math
import os
from typing import Any
from car.model import CarModelSpecification
from geometry.vector import Point
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from smart_city.road_control_center.intersection.intersection_manoeuvre_tracks.go_straight_track import (
    IntersectionGoStraightManoeuvreTrack,
)
from smart_city.road_control_center.intersection.intersection_manoeuvre_tracks.turn_left_track import (
    IntersectionTurnLeftManoeuvreTrack,
)
from smart_city.road_control_center.intersection.intersection_manoeuvre_tracks.turn_right_track import (
    IntersectionTurnRightManoeuvreTrack,
)
from smart_city.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track import (
    ManoeuvreTrack,
)
from smart_city.road_control_center.manoeuvres_preprocessing.schemas import (
    ManoeuvreTrackPoint,
    TurnSignal,
)
from smart_city.road_control_center.manoeuvres_preprocessing.track_velocities_preprocessor import (
    TrackVelocitiesPreprocessor,
)
from smart_city.schemas import IntersectionManoeuvreDescription
from utils import clockwise_direction_shift

TURN_SIGNALS_FILE_NAME = "turn_signals"


class IntersectionTrackType(Enum):
    TURN_RIGHT = "turn_right"
    GO_STRAIGHT = "go_straight"
    TURN_LEFT = "turn_left"


class IntersectionTrackVariant(Enum):
    FROM_DOWN = "from_down"
    FROM_RIGHT = "from_right"
    FROM_UP = "from_up"
    FROM_LEFT = "from_left"


INTERSECTION_SIDES_TO_VARIANTS: dict[CardinalDirection, IntersectionTrackVariant] = {
    CardinalDirection.DOWN: IntersectionTrackVariant.FROM_DOWN,
    CardinalDirection.LEFT: IntersectionTrackVariant.FROM_LEFT,
    CardinalDirection.UP: IntersectionTrackVariant.FROM_UP,
    CardinalDirection.RIGHT: IntersectionTrackVariant.FROM_RIGHT,
}


class IntersectionManoeuvresManager:
    def __init__(self, intersection: Intersection) -> None:
        self.dir_with_tracks_data = (
            "smart_city/road_control_center/preprocessed_manoeuvres_data"
        )
        self.tracks: list[tuple[IntersectionTrackType, ManoeuvreTrack]] = [
            (
                IntersectionTrackType.GO_STRAIGHT,
                IntersectionGoStraightManoeuvreTrack(
                    intersection, CardinalDirection.DOWN
                ),
            ),
            (
                IntersectionTrackType.TURN_LEFT,
                IntersectionTurnLeftManoeuvreTrack(
                    intersection, CardinalDirection.DOWN
                ),
            ),
            (
                IntersectionTrackType.TURN_RIGHT,
                IntersectionTurnRightManoeuvreTrack(
                    intersection, CardinalDirection.DOWN
                ),
            ),
        ]
        self.intersection = intersection

    def register_tracks(self) -> None:
        for track_type, manoeuvre_track in self.tracks:
            self.register_track_type_variants(track_type, manoeuvre_track)
            self.register_turn_signals(track_type, manoeuvre_track)

    def register_track_type_variants(
        self, track_type: IntersectionTrackType, manoeuvre_track: ManoeuvreTrack
    ) -> None:
        intersection_center = self.intersection.intersection_parts[
            "intersection_area"
        ].center
        for index, variant in enumerate(IntersectionTrackVariant):
            variant_track_points = [
                Point(*track_point).rotate_over_point(
                    intersection_center, math.pi / 2 * index
                )
                for track_point in manoeuvre_track.track_path
            ]
            self.register_track_type_variant(track_type, variant, variant_track_points)

    def register_track_type_variant(
        self,
        track_type: IntersectionTrackType,
        variant: IntersectionTrackVariant,
        track: list[Point],
    ) -> None:
        dir_path = os.path.join(self.dir_with_tracks_data, track_type.value)
        self.dump_json(
            dir_path,
            variant.value,
            [point.to_tuple() for point in track],
        )

    def register_turn_signals(
        self, track_type: IntersectionTrackType, manoeuvre_track: ManoeuvreTrack
    ) -> None:
        dir_path = os.path.join(self.dir_with_tracks_data, track_type.value)
        turn_signals = [
            manoeuvre_track.get_turn_signal(track_point_index).value
            for track_point_index in range(len(manoeuvre_track.track_path))
        ]
        self.dump_json(dir_path, TURN_SIGNALS_FILE_NAME, turn_signals)

    def processed_car_model_name(self, car_model_name: str) -> str:
        return car_model_name.lower().replace(" ", "_")

    def register_track_velocities(
        self, car_model_specification: CarModelSpecification
    ) -> None:
        for track_type, manoeuvre_track in self.tracks:
            max_safe_velocities = TrackVelocitiesPreprocessor().get_max_safe_velocities(
                manoeuvre_track, car_model_specification
            )
            dir_path = os.path.join(self.dir_with_tracks_data, track_type.value)
            self.dump_json(
                dir_path,
                f"{self.processed_car_model_name(car_model_specification['name'])}_velocities",
                max_safe_velocities,
            )

    def dump_json(self, dir_path: str, file_name: str, data: list[Any]) -> None:
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{file_name}.json")
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def get_track_type(
        self, manoeuvre_description: IntersectionManoeuvreDescription
    ) -> IntersectionTrackType:
        starting_side = manoeuvre_description["starting_side"]
        ending_side = manoeuvre_description["ending_side"]
        if clockwise_direction_shift(starting_side, 1) == ending_side:
            return IntersectionTrackType.TURN_LEFT
        if clockwise_direction_shift(starting_side, 3) == ending_side:
            return IntersectionTrackType.TURN_RIGHT
        return IntersectionTrackType.GO_STRAIGHT

    def load_manoeuvre_track_points(
        self,
        manoeuvre_description: IntersectionManoeuvreDescription,
        car_model_name: str,
    ) -> list[ManoeuvreTrackPoint]:
        track_type = self.get_track_type(manoeuvre_description)
        track_points = self.load_track_points(
            track_type, manoeuvre_description["starting_side"]
        )
        turn_signals = self.load_turn_signals(track_type)
        track_velocities = self.load_track_velocities(track_type, car_model_name)
        return [
            {
                "point": track_point,
                "turn_signal": turn_signal,
                "max_safe_velocity": track_velocity,
            }
            for track_point, turn_signal, track_velocity in zip(
                track_points, turn_signals, track_velocities
            )
        ]

    def load_track_velocities(
        self, track_type: IntersectionTrackType, car_model_name: str
    ) -> list[float]:
        file_path = os.path.join(
            self.dir_with_tracks_data,
            track_type.value,
            f"{self.processed_car_model_name(car_model_name)}_velocities.json",
        )
        with open(file_path, "r") as file:
            track_velocities: list[float] = json.load(file)
            return track_velocities

    def load_track_points(
        self, track_type: IntersectionTrackType, starting_side: CardinalDirection
    ) -> list[Point]:
        file_path = os.path.join(
            self.dir_with_tracks_data,
            track_type.value,
            f"{INTERSECTION_SIDES_TO_VARIANTS[starting_side].value}.json",
        )
        with open(file_path, "r") as file:
            track_points: list[tuple[float, float]] = json.load(file)
            return [Point(*point) for point in track_points]

    def load_turn_signals(self, track_type: IntersectionTrackType) -> list[TurnSignal]:
        file_path = os.path.join(
            self.dir_with_tracks_data,
            track_type.value,
            f"{TURN_SIGNALS_FILE_NAME}.json",
        )
        with open(file_path, "r") as file:
            turn_signals: list[str] = json.load(file)
            return [TurnSignal(turn_signal) for turn_signal in turn_signals]
