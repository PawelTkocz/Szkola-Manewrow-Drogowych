from road_segments.intersection.intersection import Intersection
from road_segments.intersection.schemas import IntersectionColoristics

ID = "Intersection_I0"
COLORISTICS: IntersectionColoristics = {
    "lines": "#c3dedd",
    "pavement": "#6e6362",
    "street": "#383838",
}


class IntersectionI0(Intersection):
    def __init__(self) -> None:
        super().__init__(ID, COLORISTICS)
