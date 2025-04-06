from road_segments.intersection.intersection import Intersection
from road_segments.intersection.schemas import IntersectionColors

id = "Intersection_A0"
intersection_colors: IntersectionColors = {
    "lines_color": "#c3dedd",
    "pavement_color": "#6e6362",
    "street_color": "#383838",
}
intersection_A0 = Intersection(id, intersection_colors)
