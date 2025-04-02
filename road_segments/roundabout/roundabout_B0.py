from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry import Direction, Point, Rectangle
from road_segments.roundabout.roundabout import Roundabout
from road_segments.roundabout.schemas import RoundaboutColors


id = "Roundabout_B0"
area = Rectangle(
    Point(SCREEN_WIDTH / 2, SCREEN_HEIGHT),
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    Direction(Point(0, 1)),
)
lane_width = 112
roundabout_radius = 300
central_island_radius = 25
roundabout_colors: RoundaboutColors = {
    "lines_color": "#c3dedd",
    "pavement_color": "#6e6362",
    "street_color": "#383838",
}
roundabout_B0 = Roundabout(
    id, area, lane_width, roundabout_radius, central_island_radius, roundabout_colors
)
