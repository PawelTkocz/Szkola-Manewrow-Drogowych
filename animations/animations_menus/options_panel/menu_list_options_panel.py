import pygame
from animations.animations_menus.constants import (
    FONT_COLOR,
    FONT_NAME,
    LIST_OPTION_BACKGROUND_BORDER_RADIUS,
    LIST_OPTION_BACKGROUND_COLOR,
    LIST_OPTION_BACKGROUND_TRANSPARENCY,
    LIST_OPTION_HEIGHT,
    LIST_OPTION_MIN_WIDTH,
    LIST_OPTION_TEXT_SIDE_MARGIN,
    LIST_OPTION_FONT_SIZE,
    LIST_OPTION_LEFT_OFFSET,
    LIST_OPTION_Y_SPACING,
    TITLE_TOP_OFFSET,
)
from animations.animations_menus.options_panel.menu_options_panel import (
    MenuOptionsPanel,
)
from animations.animations_menus.options_panel.schemas import ListOptionDescription
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT
from drafter.utils import blit_surface, draw_axis_aligned_rectangle
from geometry.direction import Direction
from geometry.vector import Point, Vector
from geometry.rectangle import Rectangle


class ListOption:
    def __init__(
        self,
        list_option_description: ListOptionDescription,
        rectangle: Rectangle,
    ):
        self.rectangle = rectangle
        self.on_click_app_screen_generator = list_option_description[
            "on_click_app_screen_generator"
        ]
        pygame.font.init()
        self.text_surface = pygame.font.SysFont(
            FONT_NAME, LIST_OPTION_FONT_SIZE
        ).render(list_option_description["text"], True, FONT_COLOR)
        self.text_surface_top_left = rectangle.front_left.add_vector(
            Vector(Point(0, -1))
            .scale_to_len((self.rectangle.length - self.text_surface.get_height()) // 2)
            .add_vector(Vector(Point(1, 0)).scale_to_len(LIST_OPTION_TEXT_SIDE_MARGIN))
        )

    def render(self, screen: pygame.Surface) -> None:
        draw_axis_aligned_rectangle(
            screen,
            LIST_OPTION_BACKGROUND_COLOR,
            self.rectangle.front_left,
            self.rectangle.width,
            self.rectangle.length,
            border_front_right_radius=LIST_OPTION_BACKGROUND_BORDER_RADIUS,
            border_rear_left_radius=LIST_OPTION_BACKGROUND_BORDER_RADIUS,
            border_rear_right_radius=LIST_OPTION_BACKGROUND_BORDER_RADIUS,
            transparency=LIST_OPTION_BACKGROUND_TRANSPARENCY,
        )
        blit_surface(
            screen,
            self.text_surface,
            self.text_surface_top_left,
        )

    def is_clicked(self, mouse_click_point: Point) -> bool:
        return self.rectangle.is_point_inside(mouse_click_point)

    def on_click(self) -> ApplicationScreen:
        return self.on_click_app_screen_generator()


class MenuListOptionsPanel(MenuOptionsPanel):
    def __init__(
        self,
        list_options_descriptions: list[ListOptionDescription],
    ) -> None:
        options_number = len(list_options_descriptions)
        options_panel_height = (
            options_number * LIST_OPTION_HEIGHT
            + (options_number - 1) * LIST_OPTION_Y_SPACING
        )
        pygame.font.init()
        font = pygame.font.SysFont(FONT_NAME, LIST_OPTION_FONT_SIZE)
        self.list_options_width = self._get_list_options_width(
            list_options_descriptions, font
        )
        self.options_panel = Rectangle(
            Point(
                LIST_OPTION_LEFT_OFFSET + self.list_options_width / 2,
                SCREEN_HEIGHT
                - 2 * TITLE_TOP_OFFSET
                - (SCREEN_HEIGHT - 2 * TITLE_TOP_OFFSET - options_panel_height) // 2,
            ),
            self.list_options_width,
            options_panel_height,
            Direction(Point(0, 1)),
        )
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
        font: pygame.font.Font,
    ) -> int:
        max_width = max(
            font.render(list_option["text"], True, FONT_COLOR).get_width()
            + 2 * LIST_OPTION_TEXT_SIDE_MARGIN
            for list_option in list_options_descriptions
        )
        return max(max_width, LIST_OPTION_MIN_WIDTH)

    def _calculate_list_option_rectangle(self, list_option_index: int) -> Rectangle:
        front_middle_x = self.options_panel.front_left.x + self.list_options_width / 2
        front_middle_y = self.options_panel.front_middle.y - list_option_index * (
            LIST_OPTION_HEIGHT + LIST_OPTION_Y_SPACING
        )
        return Rectangle(
            Point(front_middle_x, front_middle_y),
            self.list_options_width,
            LIST_OPTION_HEIGHT,
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
