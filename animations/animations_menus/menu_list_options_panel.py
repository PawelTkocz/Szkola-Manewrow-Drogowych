import pygame
from animations.animations_menus.constants import (
    FONT_COLOR,
    FONT_NAME,
    MENU_LIST_OPTIONS_HEIGHT,
    MENU_LIST_OPTIONS_MIN_WIDTH,
    MENU_OPTIONS_LIST_FONT_SIZE,
    MENU_OPTIONS_LIST_LEFT_OFFSET,
    MENU_OPTIONS_Y_SPACING,
    MENU_TITLE_TOP_OFFSET,
)
from animations.animations_menus.menu_options_panel import MenuOptionsPanel
from animations.animations_menus.schemas import ListOptionDescription
from application_screen.application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT
from geometry import Direction, Point, Rectangle


class ListOption:
    def __init__(
        self,
        list_option_description: ListOptionDescription,
        rectangle: Rectangle,
    ):
        self.text = list_option_description["text"]
        self.rectangle = rectangle
        self.on_click_app_screen = list_option_description["on_click_app_screen"]
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_NAME, MENU_OPTIONS_LIST_FONT_SIZE)

    def render(self, screen: pygame.Surface) -> None:
        rect_surface = pygame.Surface(
            (self.rectangle.width, self.rectangle.length), pygame.SRCALPHA
        )
        rect_surface.fill((255, 255, 255, 128))
        rect_position = (self.rectangle.front_left.x, self.rectangle.front_left.y)
        screen.blit(rect_surface, rect_position)

        text_surface = self.font.render(self.text, True, FONT_COLOR)
        # text_rect = text_surface.get_rect(
        #     center=(screen.get_width() // 2, self.title_top_offset)
        # )
        screen.blit(text_surface, rect_position)

    def is_clicked(self, mouse_click_position: tuple[float, float]) -> bool:
        return self.rectangle.is_point_inside(Point(*mouse_click_position))

    def on_click(self) -> ApplicationScreen:
        return self.on_click_app_screen


class MenuListOptionsPanel(MenuOptionsPanel):
    def __init__(
        self,
        list_options_descriptions: list[ListOptionDescription],
        *,
        height: int = SCREEN_HEIGHT,
        list_options_y_spacing: int = MENU_OPTIONS_Y_SPACING,
        list_options_left_offset: int = MENU_OPTIONS_LIST_LEFT_OFFSET,
        list_options_height: int = MENU_LIST_OPTIONS_HEIGHT,
        list_options_min_width: int = MENU_LIST_OPTIONS_MIN_WIDTH,
        title_top_offset: int = MENU_TITLE_TOP_OFFSET,
    ) -> None:
        options_number = len(list_options_descriptions)
        options_panel_height = (
            options_number * list_options_height
            + (options_number - 1) * list_options_y_spacing
        )
        pygame.font.init()
        font = pygame.font.SysFont(FONT_NAME, MENU_OPTIONS_LIST_FONT_SIZE)
        self.list_options_width = self._get_list_options_width(
            list_options_descriptions, list_options_min_width, font
        )
        self.options_panel = Rectangle(
            Point(
                list_options_left_offset + self.list_options_width / 2,
                2 * title_top_offset
                + (height - 2 * title_top_offset - options_panel_height) // 2,
            ),
            self.list_options_width,
            options_panel_height,
            Direction(Point(0, 1)),
        )
        self.list_options_y_spacing = list_options_y_spacing
        self.list_options_height = list_options_height
        self.list_options = [
            ListOption(
                list_option_description,
                self._calculate_list_option_rectangle(list_option_index),
            )
            for list_option_index, list_option_description in enumerate(
                list_options_descriptions
            )
        ]

    def _get_list_options_width(
        self,
        list_options_descriptions: list[ListOptionDescription],
        list_options_min_width: int,
        font: pygame.font.Font,
    ) -> int:
        max_width = max(
            font.render(list_option["text"], True, FONT_COLOR).get_width()
            for list_option in list_options_descriptions
        )
        return max(max_width, list_options_min_width)

    def _calculate_list_option_rectangle(self, list_option_index: int) -> Rectangle:
        front_middle_x = self.options_panel.front_left.x + self.list_options_width / 2
        front_middle_y = self.options_panel.front_middle.y - list_option_index * (
            self.list_options_height + self.list_options_y_spacing
        )
        return Rectangle(
            Point(front_middle_x, front_middle_y),
            self.list_options_width,
            self.list_options_height,
            Direction(Point(0, 1)),
        )

    def render(self, screen: pygame.Surface) -> None:
        for list_option in self.list_options:
            list_option.render(screen)

    def handle_click(
        self, mouse_click_position: tuple[float, float]
    ) -> ApplicationScreen | None:
        for list_option in self.list_options:
            if list_option.is_clicked(mouse_click_position):
                return list_option.on_click()
        return None
