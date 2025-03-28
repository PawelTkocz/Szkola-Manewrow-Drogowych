import pygame

from animations.animations_menus.constants import (
    FONT_COLOR,
    FONT_NAME,
    MENU_OPTIONS_TITLE_FONT_SIZE,
    MENU_TITLE_FONT_SIZE,
)
from animations.animations_menus.schemas import OptionItemDescription
from constants import (
    SECOND_BACKGROUND_COLOR,
)
from state import State


class OptionItem:
    def __init__(
        self,
        option_item_description: OptionItemDescription,
        rectangle: pygame.Rect,
        background_color: str,
        font: pygame.font.Font,
        font_color: str,
    ):
        self.title = option_item_description["title"]
        self.image = pygame.transform.scale(
            pygame.image.load(option_item_description["image_path"]),
            (rectangle.width, rectangle.width),
        )
        self.on_click_state = option_item_description["on_click_state"]
        self.rectangle = rectangle
        self.background_color = background_color
        self.font = font
        self.font_color = font_color

    def is_clicked(self, mouse_click_position: tuple[float, float]) -> bool:
        return self.rectangle.collidepoint(mouse_click_position)

    def on_click(self) -> State:
        return self.on_click_state

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.background_color, self.rectangle)
        screen.blit(self.image, (self.rectangle.x, self.rectangle.y))

        title_surface = self.font.render(self.title, True, self.font_color)
        title_rect = title_surface.get_rect(
            center=(
                self.rectangle.centerx,
                self.rectangle.bottom - self.font.get_height() / 2,
            )
        )
        screen.blit(title_surface, title_rect)


class OptionsMenu:
    def __init__(
        self,
        title: str,
        columns_number: int,
        height: int,
        width: int,
        title_top_offset: int,
        option_items_x_spacing: int,
        option_items_y_spacing: int,
        option_items_image_side: int,
    ) -> None:
        self.title = title

        pygame.font.init()
        self.title_font = pygame.font.SysFont(FONT_NAME, MENU_TITLE_FONT_SIZE)
        self.option_items_font = pygame.font.SysFont(
            FONT_NAME, MENU_OPTIONS_TITLE_FONT_SIZE
        )

        self.columns_number = columns_number
        self.option_items: list[OptionItem] = []
        self.height = height
        self.width = width
        self.title_top_offset = title_top_offset
        self.option_items_x_spacing = option_items_x_spacing
        self.option_items_y_spacing = option_items_y_spacing
        self.option_items_image_side = option_items_image_side

    def add_option_item(self, option_item_description: OptionItemDescription) -> None:
        self.option_items.append(
            OptionItem(
                option_item_description,
                self._calculate_option_rectangle(len(self.option_items)),
                SECOND_BACKGROUND_COLOR,
                self.option_items_font,
                FONT_COLOR,
            )
        )

    def _calculate_option_rectangle(self, option_item_index: int) -> pygame.Rect:
        options_left_offset = (
            self.width
            - (
                self.columns_number * self.option_items_image_side
                + (self.columns_number - 1) * self.option_items_x_spacing
            )
        ) // 2
        options_margin_top = 200  # fix this later

        rect_width = self.option_items_image_side
        rect_height = self.option_items_image_side + MENU_OPTIONS_TITLE_FONT_SIZE

        column = option_item_index % self.columns_number
        row = option_item_index // self.columns_number
        x_pos = options_left_offset + column * (
            rect_width + self.option_items_x_spacing
        )
        y_pos = options_margin_top + row * (rect_height + self.option_items_y_spacing)
        return pygame.Rect(x_pos, y_pos, rect_width, rect_height)

    def _render_title(self, screen: pygame.Surface) -> None:
        title_surface = self.title_font.render(self.title, True, FONT_COLOR)
        title_rect = title_surface.get_rect(
            center=(self.width // 2, self.title_top_offset)
        )
        screen.blit(title_surface, title_rect)

    def render(self, screen: pygame.Surface) -> None:
        self._render_title(screen)
        for option_item in self.option_items:
            option_item.render(screen)

    def handle_click(self, mouse_click_position: tuple[float, float]) -> State | None:
        for option_item in self.option_items:
            if option_item.is_clicked(mouse_click_position):
                return option_item.on_click()
        return None
