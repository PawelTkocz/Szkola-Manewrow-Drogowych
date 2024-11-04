from typing import List
from Geometry import Point, Vector


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
