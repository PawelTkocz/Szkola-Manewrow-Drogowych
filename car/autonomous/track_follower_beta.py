from car.autonomous.car_simulation import CarSimulation
from car.autonomous.track import Track, TrackPath
from car.autonomous.track_follower import MovementDecision, TrackFollower
from car.car_state import CarState
from car.model import CarModel
from geometry import Directions, calculate_line, distance_of_point_to_line

class UpgradedTrack(Track):
    def __init__(self, track_path: TrackPath, max_distance_in_straight_line: int):
        super().__init__(track_path)
        self.max_distance_in_straight_line = max_distance_in_straight_line
        self.furthest_point_indexes_in_line = []
        (
           self.calculate_furthest_point_indexes_in_line(max_distance_in_straight_line)
        )

    def calculate_furthest_point_index_in_line(self, start_index, max_distance):
        track_points_number = len(self.track_path)
        if start_index >= track_points_number:
            return start_index

        start_point = self.track_path[start_index]
        max_end_index = start_index  # najwiekszy indeks t.z wiemy ze dziala

        furthers_possible = track_points_number - 1  # ostatni ktory moze dzialac
        while max_end_index != furthers_possible:
            end_index = (max_end_index + furthers_possible + 1) // 2
            end_point = self.track_path[end_index]
            a, b, c = calculate_line(start_point, end_point)

            all_points_in_line = True
            for i in range(start_index + 1, end_index):
                if distance_of_point_to_line(self.track_path[i], a, b, c) > max_distance:
                    all_points_in_line = False
                    break

            if not all_points_in_line:
                furthers_possible = end_index - 1
            else:
                max_end_index = end_index
        diff = max_end_index - start_index
        if diff > 180:
            return start_index + 180
        return max_end_index
        # make this 180 some variable

    def calculate_furthest_point_indexes_in_line(self, max_distance):
        res = []
        jump = 10 * max_distance
        res.append(self.calculate_furthest_point_index_in_line(0, max_distance))
        cur_index = 0  # indeks ostatniego uzupelnionego
        while cur_index < len(self.track_path) - 1:
            jump_index = min(cur_index + jump, len(self.track_path) - 1)
            furthes_point_index = self.calculate_furthest_point_index_in_line(
                jump_index, max_distance
            )
            if furthes_point_index == res[cur_index]:
                for i in range(cur_index + 1, jump_index + 1):
                    res.append(res[-1])
            else:
                for i in range(cur_index + 1, jump_index + 1):
                    res.append(
                        self.calculate_furthest_point_index_in_line(i, max_distance)
                    )
            cur_index = jump_index
        return res

    def find_straight_line_end_point(self, track_point_index):
        return self.track_path[self.furthest_point_indexes_in_line[track_point_index]]
    
    def find_index_of_closest_point(self, point: Point):
        _, index = self.kd_tree.query([point.x, point.y])
        return index


class TrackFollowerBeta(TrackFollower):
    def __init__(self, model: CarModel):
        self.car_simulation = CarSimulation(model)

    def set_track(self, track_path: TrackPath) -> None:
        self.track_path = track_path

    def make_movement_decision(self, car_state: CarState) -> MovementDecision:
        return {"speed_modification": None, "turn_direction": None}

    def straight_lines_turning_policy(self, car_simulation: CarSimulation):
        min_distance = None
        best_turn_direction = None

        closest_point_on_track_index = (
            car_simulation.find_index_of_closest_point_on_track()
        )
        straight_line_end_point = car_simulation.find_straight_line_end_point_on_track(
            closest_point_on_track_index
        )

        for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
            start_state = car_simulation.get_state()
            car_simulation.turn(turn_direction)
            car_simulation.move()
            distance = car_simulation.find_distance_to_point(straight_line_end_point)
            if min_distance is None or distance < min_distance:
                best_turn_direction = turn_direction
                min_distance = distance
            car_simulation.set_state(start_state)

        return best_turn_direction

    def find_distance_to_point(self, point: tuple[float, float]):
        x1, y1 = point[0], point[1]
        x2, y2 = self.front_middle.x, self.front_middle.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def find_index_of_closest_point_on_track(self):
        return self.track.find_index_of_closest_point(self.front_middle)

    def find_straight_line_end_point_on_track(self, point_index):
        return self.track.find_straight_line_end_point(point_index)


#track