from typing import List
from Geometry import Point, Vector


class PartRelativePosition:
    def __init__(self, length_pos: float, width_pos: float):
        """ """
        self.length_pos = length_pos
        self.width_pos = width_pos


def get_polygon_corners(n: int, start_point: Point, vectors: List[Vector]):
    vectors_len = len(vectors)
    corners = []
    current_position = start_point.copy()
    for i in range(n):
        corners.append(current_position.copy())
        current_position.add_vector(vectors[i % vectors_len])
    return corners


def get_rectangle_corners(
    start_point: Point, front_vector: Vector, side_vector: Vector
):
    """
    Returns the corners in clockwise order
    """
    corner1 = start_point
    corner2 = corner1.copy().add_vector(front_vector)
    corner3 = corner2.copy().add_vector(side_vector)
    corner4 = corner1.copy().add_vector(side_vector)
    return [corner1, corner2, corner3, corner4]


# change name
def tuples_list(point_list: List[Point]):
    """
    Convert list of points to list of tuples
    """
    return [(p.x, p.y) for p in point_list]


def get_symmetrical_shape(
    corners: List[PartRelativePosition], symmetry_axis: float = 0.5
):
    return [
        PartRelativePosition(corner.length_pos, 2 * symmetry_axis - corner.width_pos)
        for corner in corners
    ]


def get_corners_center(corners: List[Point]):
    vector = Vector(corners[2], corners[0]).scale(0.5)
    return corners[0].copy().add_vector(vector)
