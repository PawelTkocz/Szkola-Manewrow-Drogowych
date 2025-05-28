from animations.animations_generators.intersection_I1.go_straight import (
    IntersectionI1GoStraightAnimation,
)
from animations.animations_generators.intersection_I1.turn_left import (
    IntersectionI1TurnLeftAnimation,
)
from animations.animations_generators.intersection_I1.turn_right import (
    IntersectionI1TurnRightAnimation,
)
from animations.animations_menus.options_panel.menu_list_options_panel import (
    MenuListOptionsPanel,
)
from animations.animations_menus.menu_screen import MenuScreen
from animations.animations_menus.options_panel.schemas import ListOptionDescription
from application_screen import ApplicationScreen

TITLE = "Wybierz rodzaj manewru"


class IntersectionI1ManoeuvresMenu(MenuScreen):
    def __init__(self, *, previous_app_screen: ApplicationScreen | None = None) -> None:
        list_options_descriptions: list[ListOptionDescription] = [
            {
                "text": "Skręt w prawo",
                "on_click_app_screen_generator": lambda: IntersectionI1TurnRightAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "text": "Przejazd na wprost",
                "on_click_app_screen_generator": lambda: IntersectionI1GoStraightAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "text": "Skręt w lewo",
                "on_click_app_screen_generator": lambda: IntersectionI1TurnLeftAnimation(
                    previous_app_screen=self
                ),
            },
        ]
        super().__init__(
            TITLE,
            MenuListOptionsPanel(list_options_descriptions),
            previous_app_screen=previous_app_screen,
        )
