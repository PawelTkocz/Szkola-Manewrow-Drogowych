from pygame import Surface
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT
from drafter.drafter_base import DrafterBase
from geometry import Direction, Point, Rectangle


class PreviousScreenButton:
    def __init__(
        self,
        previous_app_screen: ApplicationScreen,
        rectangle: Rectangle = Rectangle(
            Point(50, SCREEN_HEIGHT), 100, 100, Direction(Point(0, 1))
        ),
    ) -> None:
        self.previous_app_screen = previous_app_screen
        self.rectangle = rectangle

    def render(self, screen: Surface) -> None:
        DrafterBase().draw_basic_rectangle(
            screen,
            "purple",
            self.rectangle.front_left,
            self.rectangle.width,
            self.rectangle.length,
            transparency=255,
            border_front_left_radius=20,
            border_front_right_radius=20,
            border_rear_left_radius=20,
            border_rear_right_radius=20,
        )

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen | None:
        if self.rectangle.is_point_inside(mouse_click_point):
            return self.previous_app_screen
        return None
