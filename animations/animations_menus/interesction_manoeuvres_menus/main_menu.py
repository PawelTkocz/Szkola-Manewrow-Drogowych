from animations.animations_generators.intersection_I0.turn_left import (
    IntersectionI0TurnLeftAnimation,
)
from animations.animations_menus.interesction_manoeuvres_menus.intersection_I1_manoeuvres_menu import (
    IntersectionI1ManoeuvresMenu,
)
from animations.animations_menus.interesction_manoeuvres_menus.intersection_I2_manoeuvres_menu import (
    IntersectionI2ManoeuvresMenu,
)
from animations.animations_menus.interesction_manoeuvres_menus.intersection_I3_manoeuvres_menu import (
    IntersectionI3ManoeuvresMenu,
)
from animations.animations_menus.interesction_manoeuvres_menus.intersection_I4_manoeuvres_menu import (
    IntersectionI4ManoeuvresMenu,
)
from animations.animations_menus.interesction_manoeuvres_menus.intersection_I5_manoeuvres_menu import (
    IntersectionI5ManoeuvresMenu,
)
from animations.animations_menus.interesction_manoeuvres_menus.sign_A5_manoeuvres_menu import (
    IntersectionI0ManoeuvresMenu,
)
from animations.animations_menus.menu_screen import MenuScreen
from animations.animations_menus.options_panel.menu_tiles_options_panel import (
    MenuTilesOptionsPanel,
)
from animations.animations_menus.options_panel.schemas import OptionTileDescription

TITLE = "Wybierz rodzaj skrzyżowania"
OPTION_TILES_COLUMNS_NUMBER = 3


class MainMenu(MenuScreen):
    def __init__(self) -> None:
        option_tiles_descriptions: list[OptionTileDescription] = [
            {
                "image_file_name": "sign_A5.png",
                "on_click_app_screen_generator": lambda: IntersectionI0ManoeuvresMenu(
                    previous_app_screen=self
                ),
            },
            {
                "image_file_name": "sign_D1_and_A7.png",
                "on_click_app_screen_generator": lambda: IntersectionI1ManoeuvresMenu(
                    previous_app_screen=self
                ),
            },
            {
                "image_file_name": "sign_B20.png",
                "on_click_app_screen_generator": lambda: IntersectionI2ManoeuvresMenu(
                    previous_app_screen=self
                ),
            },
            {
                "image_file_name": "sign_T6a.png",
                "on_click_app_screen_generator": lambda: IntersectionI3ManoeuvresMenu(
                    previous_app_screen=self
                ),
            },
            {
                "image_file_name": "traffic_lights.png",
                "on_click_app_screen_generator": lambda: IntersectionI4ManoeuvresMenu(
                    previous_app_screen=self
                ),
            },
            {
                "image_file_name": "traffic_lights_arrow.png",
                "on_click_app_screen_generator": lambda: IntersectionI5ManoeuvresMenu(
                    previous_app_screen=self
                ),
            },
        ]
        super().__init__(
            TITLE,
            MenuTilesOptionsPanel(
                OPTION_TILES_COLUMNS_NUMBER, option_tiles_descriptions
            ),
        )
