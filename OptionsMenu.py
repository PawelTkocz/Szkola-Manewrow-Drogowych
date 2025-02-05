from typing import TypedDict
import pygame

from Constants import (
    OPTIONS_SCREENSHOT_SIZE,
    SCREEN_WIDTH,
    SECOND_BACKGROUND_COLOR,
)
from OptionToChoose import OptionToChoose
from State import State


OPTIONS_FONT_SIZE = 40
OPTIONS_X_SPACING = 80
OPTIONS_Y_SPACING = 50
OPTIONS_OFFSET_Y = 200
TEXT_COLOR = "#000000"
DEFAULT_FONT = "Sofia Pro"
TITLE_FONT_SIZE = 120
TITLE_OFFSET_Y = 100


class Option(TypedDict):
    option_to_choose: OptionToChoose
    rect: pygame.Rect


class OptionsMenu:
    def __init__(self, title, columns_number):
        self.title = title

        pygame.font.init()
        self.title_font = pygame.font.SysFont(DEFAULT_FONT, TITLE_FONT_SIZE)
        self.options_font = pygame.font.SysFont(DEFAULT_FONT, OPTIONS_FONT_SIZE)

        self.columns_number = columns_number
        self.options: list[Option] = []

        self.options_margin_left = (
            SCREEN_WIDTH
            - (
                columns_number * OPTIONS_SCREENSHOT_SIZE
                + (columns_number - 1) * OPTIONS_X_SPACING
            )
        ) // 2
        self.options_margin_top = OPTIONS_OFFSET_Y

    def add_option_to_choose(self, option_to_choose: OptionToChoose):
        self.options.append(
            {
                "option_to_choose": option_to_choose,
                "rect": self._calculate_option_rectangle(),
            }
        )

    def _calculate_option_rectangle(self):
        rect_width = OPTIONS_SCREENSHOT_SIZE
        rect_height = OPTIONS_SCREENSHOT_SIZE + OPTIONS_FONT_SIZE

        option_index = len(self.options)
        column = option_index % self.columns_number
        row = option_index // self.columns_number
        x_pos = self.options_margin_left + column * (rect_width + OPTIONS_X_SPACING)
        y_pos = self.options_margin_top + row * (rect_height + OPTIONS_Y_SPACING)

        return pygame.Rect(x_pos, y_pos, rect_width, rect_height)

    def _render_title(self, screen):
        title_surface = self.title_font.render(self.title, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, TITLE_OFFSET_Y))
        screen.blit(title_surface, title_rect)

    def _render_options(self, screen):
        for option in self.options:
            rect = option["rect"]
            pygame.draw.rect(screen, SECOND_BACKGROUND_COLOR, rect)
            screen.blit(option["option_to_choose"].image, (rect.x, rect.y))

            option_title_surface = self.options_font.render(
                option["option_to_choose"].title, True, TEXT_COLOR
            )
            option_title_rect = option_title_surface.get_rect(
                center=(
                    rect.x + rect.width // 2,
                    rect.y + rect.height - OPTIONS_FONT_SIZE / 2,
                )
            )
            screen.blit(option_title_surface, option_title_rect)

    def render(self, screen):
        self._render_title(screen)
        self._render_options(screen)

    def handle_click(self, mouse_click_position) -> State | None:
        for option in self.options:
            rect = option["rect"]
            if rect.collidepoint(mouse_click_position):
                option_title = option["option_to_choose"].title
                print(f"clicked on option {option_title}")
                return option["option_to_choose"].on_click()
        return None
