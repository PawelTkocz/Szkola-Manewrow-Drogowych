from pygame import Surface

from geometry.shapes.rectangle import AxisAlignedRectangle
from geometry.vector import Point, Vector


def get_fitted_surface_rectangle(
    surface: Surface,
    bounding_rectangle: AxisAlignedRectangle,
) -> AxisAlignedRectangle:
    surface_aspect_ratio = surface.get_width() / surface.get_height()

    bounding_width = bounding_rectangle.width
    bounding_height = bounding_rectangle.length
    bounding_aspect_ratio = bounding_width / bounding_height

    if surface_aspect_ratio > bounding_aspect_ratio:
        fitted_width = bounding_width
        fitted_height = fitted_width / surface_aspect_ratio
    else:
        fitted_height = bounding_height
        fitted_width = fitted_height * surface_aspect_ratio

    fitted_front_middle = bounding_rectangle.front_middle.add_vector(
        Vector(Point(0, -1)).scale_to_len((bounding_height - fitted_height) / 2)
    )

    return AxisAlignedRectangle(fitted_front_middle, fitted_width, fitted_height)
