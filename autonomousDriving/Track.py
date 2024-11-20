from scipy.spatial import KDTree

from Geometry import Point, calculate_line, distance_of_point_to_line


class Track:
    """
    Class representing track as a list of points
    """

    def __init__(self, track: list[tuple[float, float]], max_distance_in_straight_line):
        self.track = track
        self.kd_tree = KDTree(track)
        self.max_distance_in_straight_line = max_distance_in_straight_line
        self.furthest_point_indexes_in_line = (
            self.calculate_furthest_point_indexes_in_line(max_distance_in_straight_line)
        )

    def calculate_furthest_point_index_in_line(self, start_index, max_distance):
        track_points_number = len(self.track)
        if start_index >= track_points_number:
            return start_index

        start_point = self.track[start_index]
        max_end_index = start_index  # najwiekszy indeks t.z wiemy ze dziala

        furthers_possible = track_points_number - 1  # ostatni ktory moze dzialac
        while max_end_index != furthers_possible:
            end_index = (max_end_index + furthers_possible + 1) // 2
            end_point = self.track[end_index]
            a, b, c = calculate_line(start_point, end_point)

            all_points_in_line = True
            for i in range(start_index + 1, end_index):
                if distance_of_point_to_line(self.track[i], a, b, c) > max_distance:
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
        jump = 2 * max_distance
        res.append(self.calculate_furthest_point_index_in_line(0, max_distance))
        cur_index = 0  # indeks ostatniego uzupelnionego
        while cur_index < len(self.track) - 1:
            jump_index = min(cur_index + jump, len(self.track) - 1)
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

    def find_distance_to_point(self, point: Point):
        distances, _ = self.kd_tree.query([point.x, point.y], k=2)
        return distances[0] + distances[1]

    def find_index_of_closest_point(self, point: Point):
        _, index = self.kd_tree.query([point.x, point.y])
        return index

    def find_straight_line_end_point(self, track_point_index):
        return self.track[self.furthest_point_indexes_in_line[track_point_index]]
