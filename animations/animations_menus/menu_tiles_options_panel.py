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
from geometry import Direction, Point, Rectangle


class OptionTile:
    def __init__(
        self,
        tile_description: OptionTileDescription,
        rectangle: Rectangle,
    ):
        self.image_path = tile_description["image_path"]  # to delete
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
        rect_surface = pygame.Surface(
            (self.rectangle.width, self.rectangle.length), pygame.SRCALPHA
        )
        rect_surface.fill((255, 255, 255, 128))
        rect_position = (self.rectangle.front_left.x, self.rectangle.front_left.y)
        screen.blit(rect_surface, rect_position)
        screen.blit(self.image, rect_position)

    def is_clicked(self, mouse_click_position: tuple[float, float]) -> bool:
        return self.rectangle.is_point_inside(Point(*mouse_click_position))

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
                2 * title_top_offset
                + (height - 2 * title_top_offset - options_panel_height) // 2,
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

    def handle_click(
        self, mouse_click_position: tuple[float, float]
    ) -> ApplicationScreen | None:
        mouse_click_position = (
            mouse_click_position[0],
            SCREEN_HEIGHT - mouse_click_position[1],
        )
        for option_tile in self.option_tiles:
            print([(a.x, a.y) for a in option_tile.rectangle.corners_list])
            if option_tile.is_clicked(mouse_click_position):
                print(option_tile.image_path)
                return option_tile.on_click()
        return None
