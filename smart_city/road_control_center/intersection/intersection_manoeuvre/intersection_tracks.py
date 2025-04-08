from enum import Enum
import json
import math
import os
from typing import TypedDict
from car.model import CarModel
from car.toyota_yaris import ToyotaYaris
from geometry import Cooridinates, Direction, Point
from road_segments.intersection import intersection_A0
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection, HorizontalDirection, VerticalDirection
from smart_city.road_control_center.intersection.intersection_manoeuvre.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.road_control_center.manoeuvres.schemas import TrackPointData, TurnSignal
from smart_city.road_control_center.manoeuvres.track_preprocessor.manoeuvre_track import (
    ManoeuvreTrack,
)
from smart_city.road_control_center.manoeuvres.track_preprocessor.manoeuvre_track_segment import (
    TrackSegmentType,
)
from smart_city.road_control_center.manoeuvres.track_preprocessor.right_angle_turn import (
    RightAngleTurn,
)
from smart_city.road_control_center.manoeuvres.track_preprocessor.straight_path import (
    StraightPath,
)

EXPECTED_MIN_TURN_VELOCITY = 2


class IntersectionTrackPoint(TypedDict):
    from_left: Cooridinates
    from_right: Cooridinates
    from_up: Cooridinates
    from_down: Cooridinates
    turn_signal: str


class IntersectionTrackType(Enum):
    TURN_RIGHT = "turn_right"
    GO_STRAIGHT = "go_straight"
    TURN_LEFT = "turn_left"


class IntersectionTracks:
    def __init__(self, intersection: Intersection, car_model: CarModel) -> None:
        self.intersection = intersection
        self.car_model = car_model
        self.tracks_dir_path = f"smart_city/road_control_center/intersection/intersection_manoeuvre/tracks/{self.intersection.id}/tracks"

    def register_tracks(self) -> None:
        tracks = [
            (IntersectionTrackType.TURN_LEFT, self.calculate_track_from_down_to_left()),
            (
                IntersectionTrackType.TURN_RIGHT,
                self.calculate_track_from_down_to_right(),
            ),
            (IntersectionTrackType.GO_STRAIGHT, self.calculate_track_from_down_to_up()),
        ]
        os.makedirs(self.tracks_dir_path, exist_ok=True)
        for track_type, manoeuvre_track in tracks:
            self.register_track(track_type, manoeuvre_track)

    def register_track(
        self, track_type: IntersectionTrackType, manoeuvre_track: ManoeuvreTrack
    ) -> None:
        file_path = os.path.join(
            self.tracks_dir_path,
            f"{track_type.value}.json",
        )
        serialized_track = self.serialize_track(manoeuvre_track)
        with open(
            file_path,
            "w",
        ) as f:
            json.dump(serialized_track, f, indent=4)

    def calculate_track_from_down_to_left(self) -> ManoeuvreTrack:
        return self.calculate_turn_track_from_down(HorizontalDirection.LEFT, 0)

    def calculate_track_from_down_to_right(self) -> ManoeuvreTrack:
        return self.calculate_turn_track_from_down(
            HorizontalDirection.RIGHT, self.car_model.length
        )

    def calculate_turn_track_from_down(
        self,
        ending_side_horizontal: HorizontalDirection,
        start_turn_offset: float,
    ) -> ManoeuvreTrack:
        starting_side = CardinalDirection.DOWN
        ending_side = (
            CardinalDirection.LEFT
            if ending_side_horizontal == HorizontalDirection.LEFT
            else CardinalDirection.RIGHT
        )
        turn_direction = ending_side_horizontal
        incoming_lane = self.intersection.intersection_parts["incoming_lines"][
            starting_side
        ]
        start_point = incoming_lane.rear_middle
        outcoming_lane = self.intersection.intersection_parts["outcoming_lines"][
            ending_side
        ]
        end_point = outcoming_lane.front_middle.add_vector(
            outcoming_lane.direction.scale_to_len(2 * self.car_model.length)
        )
        start_turn_point = incoming_lane.front_middle.add_vector(
            incoming_lane.direction.get_negative_of_a_vector().scale_to_len(
                start_turn_offset
            )
        )
        end_turn_point = outcoming_lane.rear_middle.add_vector(
            outcoming_lane.direction.scale_to_len(start_turn_offset)
        )
        return ManoeuvreTrack(
            [
                StraightPath(start_point, start_turn_point),
                RightAngleTurn(
                    start_turn_point,
                    end_turn_point,
                    turn_direction,
                    EXPECTED_MIN_TURN_VELOCITY,
                ),
                StraightPath(end_turn_point, end_point),
            ],
            {
                "direction": Direction(Point(1, 0)),
                "front_middle": Point(0, 0),
                "wheels_direction": Direction(Point(1, 0)),
            },
        )

    def calculate_track_from_down_to_up(self) -> ManoeuvreTrack:
        starting_side = CardinalDirection.DOWN
        ending_side = CardinalDirection.UP
        start_point = self.intersection.intersection_parts["incoming_lines"][
            starting_side
        ].rear_middle
        outcoming_lane = self.intersection.intersection_parts["outcoming_lines"][
            ending_side
        ]
        end_point = outcoming_lane.front_middle.add_vector(
            outcoming_lane.direction.scale_to_len(2 * self.car_model.length)
        )
        return ManoeuvreTrack(
            [StraightPath(start_point, end_point)],
            {
                "direction": Direction(Point(1, 0)),
                "front_middle": Point(0, 0),
                "wheels_direction": Direction(Point(1, 0)),
            },
        )

    def get_track_type(
        self, manoeuvre_description: IntersectionManoeuvreDescription
    ) -> IntersectionTrackType:
        starting_side = manoeuvre_description["starting_side"]
        ending_side = manoeuvre_description["ending_side"]
        vertical_sides = [CardinalDirection.UP, CardinalDirection.DOWN]
        horizontal_sides = [CardinalDirection.LEFT, CardinalDirection.RIGHT]
        if (starting_side in vertical_sides and ending_side in vertical_sides) or (
            starting_side in horizontal_sides and ending_side in horizontal_sides
        ):
            return IntersectionTrackType.GO_STRAIGHT
        directions = list(CardinalDirection)
        starting_side_index = directions.index(starting_side)
        if directions[(starting_side_index + 1) % 4] == ending_side:
            return IntersectionTrackType.TURN_LEFT
        else:
            return IntersectionTrackType.TURN_RIGHT

    def get_track_points_data(
        self,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ) -> list[TrackPointData]:
        track_type = self.get_track_type(manoeuvre_description)
        with open(
            f"smart_city/road_control_center/intersection/intersection_manoeuvre/tracks/{self.intersection.id}/tracks/{track_type.value}.json",
            "r",
        ) as file:
            intersection_track_points: list[IntersectionTrackPoint] = json.load(file)
            return [
                {
                    "point": Point(point["from_down"]["x"], point["from_down"]["y"]),
                    "turn_signal": TurnSignal(point["turn_signal"]),
                    "max_safe_velocity": 10,
                }
                for point in intersection_track_points
            ]

    def get_turn_signal_for_track_point(
        self, track_point: Point, track: ManoeuvreTrack
    ) -> TurnSignal:
        track_point_index = track.find_index_of_closest_point(track_point)
        incoming_segments_data = track.get_incoming_segments_data(track_point_index)
        if (
            incoming_segments_data["current_track_segment"].type
            == TrackSegmentType.TURN_LEFT
        ):
            return TurnSignal.LEFT_SIGNAL
        elif (
            incoming_segments_data["current_track_segment"].type
            == TrackSegmentType.TURN_RIGHT
        ):
            return TurnSignal.RIGHT_SIGNAL
        return TurnSignal.NO_SIGNAL

    def serialize_track(
        self, track_from_down: ManoeuvreTrack
    ) -> list[IntersectionTrackPoint]:
        track_path = track_from_down.track_path
        intersection_center = self.intersection.intersection_parts[
            "intersection_area"
        ].center
        serialized_track: list[IntersectionTrackPoint] = []
        for x, y in track_path:
            point_from_down = Point(x, y)
            point_from_right = point_from_down.copy().rotate_over_point(
                intersection_center, math.pi / 2
            )
            point_from_up = point_from_down.copy().rotate_over_point(
                intersection_center, math.pi
            )
            point_from_left = point_from_down.copy().rotate_over_point(
                intersection_center, -1 * math.pi / 2
            )
            turn_signal = self.get_turn_signal_for_track_point(
                point_from_down, track_from_down
            )
            serialized_track.append(
                {
                    "from_down": point_from_down.to_dict(),
                    "from_left": point_from_left.to_dict(),
                    "from_right": point_from_right.to_dict(),
                    "from_up": point_from_up.to_dict(),
                    "turn_signal": turn_signal.value,
                }
            )
        return serialized_track


c = IntersectionTracks(intersection_A0.intersection_A0, ToyotaYaris())
c.register_tracks()
