from animations.animations_generators.intersection.go_straight import (
    IntersectionGoStraightAnimation,
)
from animations.animations_generators.intersection.turn_left import (
    IntersectionTurnLeftAnimation,
)
from animations.animations_generators.intersection.turn_right import (
    IntersectionTurnRightAnimation,
)
from animations.animations_menus.constants import (
    MAIN_MENU_OPTIONS_COLUMNS_NUMBER,
    MAIN_MENU_TITLE,
)
from animations.animations_menus.interesction_manoeuvres_menus.sign_A5_manoeuvres_menu import (
    SignA5ManoeuvresMenu,
)
from animations.animations_menus.menu_screen import MenuScreen
from animations.animations_menus.menu_tiles_options_panel import MenuTilesOptionsPanel
from animations.animations_menus.schemas import OptionTileDescription


class MainMenu(MenuScreen):
    def __init__(self) -> None:
        option_tiles_descriptions: list[OptionTileDescription] = [
            {
                "image_path": "animations/animations_menus/screenshots/sign_A5.png",
                "on_click_app_screen": SignA5ManoeuvresMenu(self),
            },
            {
                "image_path": "animations/animations_menus/screenshots/sign_D1_and_A7.png",
                "on_click_app_screen": IntersectionTurnRightAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "image_path": "animations/animations_menus/screenshots/sign_B20.png",
                "on_click_app_screen": IntersectionGoStraightAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "image_path": "animations/animations_menus/screenshots/sign_T6a.png",
                "on_click_app_screen": IntersectionTurnLeftAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "image_path": "animations/animations_menus/screenshots/traffic_lights.png",
                "on_click_app_screen": IntersectionTurnLeftAnimation(
                    previous_app_screen=self
                ),
            },
            {
                "image_path": "animations/animations_menus/screenshots/traffic_lights_arrow.png",
                "on_click_app_screen": IntersectionTurnLeftAnimation(
                    previous_app_screen=self
                ),
            },
        ]
        super().__init__(
            MAIN_MENU_TITLE,
            MenuTilesOptionsPanel(
                MAIN_MENU_OPTIONS_COLUMNS_NUMBER, option_tiles_descriptions
            ),
        )
