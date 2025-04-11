import pygame
from animations.animations_menus.constants import (
    FONT_COLOR,
    FONT_NAME,
    MENU_LIST_OPTIONS_HEIGHT,
    MENU_LIST_OPTIONS_MIN_WIDTH,
    MENU_LIST_OPTIONS_TEXT_LEFT_OFFSET,
    MENU_OPTIONS_LIST_FONT_SIZE,
    MENU_OPTIONS_LIST_LEFT_OFFSET,
    MENU_OPTIONS_Y_SPACING,
    MENU_TITLE_TOP_OFFSET,
)
from animations.animations_menus.menu_options_panel import MenuOptionsPanel
from animations.animations_menus.schemas import ListOptionDescription
from application_screen.application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT
from drafter.drafter_base import DrafterBase
from geometry import Direction, Point, Rectangle, Vector


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
        DrafterBase().draw_basic_rectangle(
            screen,
            "white",
            self.rectangle.front_left,
            self.rectangle.width,
            self.rectangle.length,
            border_front_right_radius=10,
            border_rear_left_radius=10,
            border_rear_right_radius=10,
            transparency=190,
        )
        text_surface = self.font.render(self.text, True, FONT_COLOR)
        DrafterBase().blit_surface(
            screen,
            text_surface,
            self.rectangle.front_left.add_vector(
                Vector(Point(0, -1))
                .scale_to_len((self.rectangle.length - text_surface.get_height()) / 2)
                .add_vector(
                    Vector(Point(1, 0)).scale_to_len(MENU_LIST_OPTIONS_TEXT_LEFT_OFFSET)
                )
            ),
        )

    def is_clicked(self, mouse_click_point: Point) -> bool:
        return self.rectangle.is_point_inside(mouse_click_point)

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
                height
                - 2 * title_top_offset
                - (height - 2 * title_top_offset - options_panel_height) // 2,
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
            + MENU_LIST_OPTIONS_TEXT_LEFT_OFFSET
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

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen | None:
        for list_option in self.list_options:
            if list_option.is_clicked(mouse_click_point):
                return list_option.on_click()
        return None
