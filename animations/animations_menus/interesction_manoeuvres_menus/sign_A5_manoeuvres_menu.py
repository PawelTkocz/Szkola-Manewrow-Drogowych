from animations.animations_generators.intersection.go_straight import (
    IntersectionGoStraightAnimation,
)
from animations.animations_generators.intersection.turn_left import (
    IntersectionTurnLeftAnimation,
)
from animations.animations_generators.intersection.turn_right import (
    IntersectionTurnRightAnimation,
)
from animations.animations_menus.constants import INTERSECTION_MENU_TITLE
from animations.animations_menus.menu_list_options_panel import MenuListOptionsPanel
from animations.animations_menus.menu_screen import MenuScreen
from animations.animations_menus.schemas import ListOptionDescription
from application_screen import ApplicationScreen


class SignA5ManoeuvresMenu(MenuScreen):
    def __init__(self, previous_app_screen: ApplicationScreen | None = None) -> None:
        list_options_descriptions: list[ListOptionDescription] = [
            {
                "text": "Skret w prawo",
                "on_click_app_screen": IntersectionTurnRightAnimation(self),
            },
            {
                "text": "Przejazd na wprost",
                "on_click_app_screen": IntersectionGoStraightAnimation(self),
            },
            {
                "text": "Skret w lewo",
                "on_click_app_screen": IntersectionTurnLeftAnimation(self),
            },
        ]
        super().__init__(
            INTERSECTION_MENU_TITLE,
            MenuListOptionsPanel(list_options_descriptions),
            previous_app_screen=previous_app_screen,
        )
