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
from application_screen.application_screen import ApplicationScreen
from application_screen.back_navigable_application_screen import (
    BackNavigableApplicationScreen,
)


class SignA5ManoeuvresScreen(MenuScreen):
    def __init__(self) -> None:
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
            INTERSECTION_MENU_TITLE, MenuListOptionsPanel(list_options_descriptions)
        )


class SignA5ManoeuvresMenu(BackNavigableApplicationScreen):
    def __init__(self, previous_app_screen: ApplicationScreen) -> None:
        super().__init__(SignA5ManoeuvresScreen(), previous_app_screen)
