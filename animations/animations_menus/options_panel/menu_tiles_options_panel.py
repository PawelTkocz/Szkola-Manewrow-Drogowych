import math
import pygame
from animations.animations_menus.constants import (
    OPTION_TILE_BACKGROUND_BORDER_RADIUS,
    OPTION_TILE_BACKGROUND_COLOR,
    OPTION_TILE_BACKGROUND_TRANSPARENCY,
    OPTION_TILE_SIDE,
    OPTION_TILE_X_SPACING,
    OPTION_TILE_Y_SPACING,
    TITLE_TOP_OFFSET,
)
from animations.animations_menus.options_panel.menu_options_panel import (
    MenuOptionsPanel,
)
from animations.animations_menus.options_panel.schemas import (
    OptionTileDescription,
)
from animations.constants import IMAGES_DIR_PATH
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from drafter.utils import blit_surface, draw_axis_aligned_rectangle
from geometry import Direction, Point, Rectangle


class OptionTile:
    def __init__(
        self,
        tile_description: OptionTileDescription,
        rectangle: Rectangle,
    ):
        self.image = pygame.transform.scale(
            pygame.image.load(
                f"{IMAGES_DIR_PATH}/{tile_description['image_file_name']}"
            ),
            (rectangle.width, rectangle.length),
        )
        self.rectangle = rectangle
        self.on_click_app_screen_generator = tile_description[
            "on_click_app_screen_generator"
        ]

    def render(self, screen: pygame.Surface) -> None:
        draw_axis_aligned_rectangle(
            screen,
            OPTION_TILE_BACKGROUND_COLOR,
            self.rectangle.front_left,
            self.rectangle.width,
            self.rectangle.length,
            border_front_left_radius=OPTION_TILE_BACKGROUND_BORDER_RADIUS,
            border_front_right_radius=OPTION_TILE_BACKGROUND_BORDER_RADIUS,
            border_rear_left_radius=OPTION_TILE_BACKGROUND_BORDER_RADIUS,
            border_rear_right_radius=OPTION_TILE_BACKGROUND_BORDER_RADIUS,
            transparency=OPTION_TILE_BACKGROUND_TRANSPARENCY,
        )
        blit_surface(screen, self.image, self.rectangle.front_left)

    def is_clicked(self, mouse_click_point: Point) -> bool:
        return self.rectangle.is_point_inside(mouse_click_point)

    def on_click(self) -> ApplicationScreen:
        return self.on_click_app_screen_generator()


class MenuTilesOptionsPanel(MenuOptionsPanel):
    def __init__(
        self,
        columns_number: int,
        option_tiles_description: list[OptionTileDescription],
    ) -> None:
        rows_number = math.ceil(len(option_tiles_description) / columns_number)
        options_panel_height = (
            rows_number * OPTION_TILE_SIDE + (rows_number - 1) * OPTION_TILE_Y_SPACING
        )
        self.options_panel = Rectangle(
            Point(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT
                - 2 * TITLE_TOP_OFFSET
                - (SCREEN_HEIGHT - 2 * TITLE_TOP_OFFSET - options_panel_height) // 2,
            ),
            columns_number * OPTION_TILE_SIDE
            + (columns_number - 1) * OPTION_TILE_X_SPACING,
            options_panel_height,
            Direction(Point(0, 1)),
        )
        self.columns_number = columns_number
        self.option_tiles = [
            OptionTile(tile_description, self._calculate_tile_rectangle(tile_index))
            for tile_index, tile_description in enumerate(option_tiles_description)
        ]

    def _calculate_tile_rectangle(self, option_tile_index: int) -> Rectangle:
        column = option_tile_index % self.columns_number
        row = option_tile_index // self.columns_number
        front_middle_x = (
            self.options_panel.front_left.x
            + column * (OPTION_TILE_SIDE + OPTION_TILE_X_SPACING)
            + OPTION_TILE_SIDE // 2
        )
        front_middle_y = self.options_panel.front_middle.y - row * (
            OPTION_TILE_SIDE + OPTION_TILE_Y_SPACING
        )
        return Rectangle(
            Point(front_middle_x, front_middle_y),
            OPTION_TILE_SIDE,
            OPTION_TILE_SIDE,
            Direction(Point(0, 1)),
        )

    def render(self, screen: pygame.Surface) -> None:
        for option_tile in self.option_tiles:
            option_tile.render(screen)

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen | None:
        for option_tile in self.option_tiles:
            if option_tile.is_clicked(mouse_click_point):
                return option_tile.on_click()
        return None
