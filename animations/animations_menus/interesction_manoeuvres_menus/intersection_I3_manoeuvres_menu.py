from animations.animations_generators.intersection_I3.go_straight import (
    IntersectionI3GoStraightAnimation,
)
from animations.animations_generators.intersection_I3.turn_left import (
    IntersectionI3TurnLeftAnimation,
)
from animations.animations_generators.intersection_I3.turn_right import (
    IntersectionI3TurnRightAnimation,
)
from animations.animations_menus.options_panel.menu_list_options_panel import (
    MenuListOptionsPanel,
)
from animations.animations_menus.menu_screen import MenuScreen
from animations.animations_menus.options_panel.schemas import ListOptionDescription
from application_screen import ApplicationScreen

TITLE = "Wybierz rodzaj manewru"


class IntersectionI3ManoeuvresMenu(MenuScreen):
    def __init__(self, *, previous_app_screen: ApplicationScreen | None = None) -> None:
        list_options_descriptions: list[ListOptionDescription] = [
            {
                "text": "Skret w prawo",
                "on_click_app_screen_generator": lambda: IntersectionI3TurnRightAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "text": "Przejazd na wprost",
                "on_click_app_screen_generator": lambda: IntersectionI3GoStraightAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "text": "Skret w lewo",
                "on_click_app_screen_generator": lambda: IntersectionI3TurnLeftAnimation(
                    previous_app_screen=self
                ),
            },
        ]
        super().__init__(
            TITLE,
            MenuListOptionsPanel(list_options_descriptions),
            previous_app_screen=previous_app_screen,
        )
