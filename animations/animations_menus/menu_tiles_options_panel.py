import math
import pygame
from animations.animations_menus.constants import (
    MENU_TILES_SIDE,
    MENU_TILES_X_SPACING,
    MENU_TILES_Y_SPACING,
    MENU_TITLE_TOP_OFFSET,
)
from animations.animations_menus.menu_options_panel import MenuOptionsPanel
from animations.animations_menus.schemas import (
    OptionTileDescription,
)
from application_screen.application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from drafter.drafter_base import DrafterBase
from geometry import Direction, Point, Rectangle


class OptionTile:
    def __init__(
        self,
        tile_description: OptionTileDescription,
        rectangle: Rectangle,
    ):
        self.image = self.get_image(tile_description["image_path"], rectangle)
        self.rectangle = rectangle
        self.on_click_app_screen = tile_description["on_click_app_screen"]

    def get_image(self, image_path: str, rectangle: Rectangle) -> pygame.Surface:
        original_image = pygame.image.load(image_path)
        original_image_rect = original_image.get_rect()
        max_size = rectangle.width
        scale = min(
            max_size / original_image_rect.width, max_size / original_image_rect.height
        )
        return pygame.transform.scale(
            original_image,
            (
                int(original_image_rect.width * scale),
                int(original_image_rect.height * scale),
            ),
        )

    def render(self, screen: pygame.Surface) -> None:
        DrafterBase().draw_basic_rectangle(
            screen,
            "white",
            self.rectangle.front_left,
            self.rectangle.width,
            self.rectangle.length,
            border_front_left_radius=20,
            border_front_right_radius=20,
            border_rear_left_radius=20,
            border_rear_right_radius=20,
            transparency=164,
        )
        DrafterBase().blit_surface(screen, self.image, self.rectangle.front_left)

    def is_clicked(self, mouse_click_point: Point) -> bool:
        return self.rectangle.is_point_inside(mouse_click_point)

    def on_click(self) -> ApplicationScreen:
        return self.on_click_app_screen


class MenuTilesOptionsPanel(MenuOptionsPanel):
    def __init__(
        self,
        columns_number: int,
        option_tiles_description: list[OptionTileDescription],
        height: int = SCREEN_HEIGHT,
        width: int = SCREEN_WIDTH,
        tile_x_spacing: int = MENU_TILES_X_SPACING,
        tile_y_spacing: int = MENU_TILES_Y_SPACING,
        tile_side: int = MENU_TILES_SIDE,
        title_top_offset: int = MENU_TITLE_TOP_OFFSET,
    ) -> None:
        rows_number = math.ceil(len(option_tiles_description) / columns_number)
        options_panel_height = (
            rows_number * tile_side + (rows_number - 1) * tile_y_spacing
        )
        self.options_panel = Rectangle(
            Point(
                width // 2,
                height
                - 2 * title_top_offset
                - (height - 2 * title_top_offset - options_panel_height) // 2,
            ),
            columns_number * tile_side + (columns_number - 1) * tile_x_spacing,
            options_panel_height,
            Direction(Point(0, 1)),
        )
        self.columns_number = columns_number
        self.tile_x_spacing = tile_x_spacing
        self.tile_y_spacing = tile_y_spacing
        self.tile_side = tile_side
        self.option_tiles = [
            OptionTile(tile_description, self._calculate_tile_rectangle(tile_index))
            for tile_index, tile_description in enumerate(option_tiles_description)
        ]

    def _calculate_tile_rectangle(self, option_tile_index: int) -> Rectangle:
        column = option_tile_index % self.columns_number
        row = option_tile_index // self.columns_number
        front_middle_x = (
            self.options_panel.front_left.x
            + column * (self.tile_side + self.tile_x_spacing)
            + self.tile_side // 2
        )
        front_middle_y = self.options_panel.front_middle.y - row * (
            self.tile_side + self.tile_y_spacing
        )
        return Rectangle(
            Point(front_middle_x, front_middle_y),
            self.tile_side,
            self.tile_side,
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
