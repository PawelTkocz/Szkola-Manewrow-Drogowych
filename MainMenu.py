import pygame

from Constants import (
    BACKGROUND_COLOR,
    DEFAULT_FONT,
    OPTIONS_BOX_MARGIN,
    OPTIONS_FONT_SIZE,
    OPTIONS_OFFSET_Y,
    OPTIONS_SCREENSHOT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SECOND_BACKGROUND_COLOR,
    TEXT_COLOR,
    TITLE_FONT_SIZE,
    TITLE_OFFSET_Y,
)

pygame.font.init()


class MainMenu:
    def __init__(self):
        self.title_font = pygame.font.SysFont(DEFAULT_FONT, TITLE_FONT_SIZE)
        self.option_font = pygame.font.SysFont(DEFAULT_FONT, OPTIONS_FONT_SIZE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.options_rows = 2
        self.options_columns = 3
        self.animations_options = [
            {
                "title": "Animation 1",
                "screenshot": "animationsScreenshots/screenshot1.png",
            },
            {
                "title": "Animation 2",
                "screenshot": "animationsScreenshots/screenshot2.png",
            },
            {
                "title": "Animation 3",
                "screenshot": "animationsScreenshots/screenshot3.png",
            },
            {
                "title": "Animation 4",
                "screenshot": "animationsScreenshots/screenshot4.png",
            },
            {
                "title": "Animation 5",
                "screenshot": "animationsScreenshots/screenshot5.png",
            },
            {
                "title": "Animation 6",
                "screenshot": "animationsScreenshots/screenshot6.png",
            },
        ]
        self.read_animations_images()
        self.calculate_animations_rectangles()

    def load_screenshot(self, path):
        try:
            return pygame.image.load(path)
        except pygame.error:
            return pygame.Surface((OPTIONS_SCREENSHOT_SIZE, OPTIONS_SCREENSHOT_SIZE))

    def draw_title(self):
        title_surface = self.title_font.render("Choose Animation", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, TITLE_OFFSET_Y))
        self.screen.blit(title_surface, title_rect)

    def read_animations_images(self):
        for animation in self.animations_options:
            animation["image"] = pygame.transform.scale(
                self.load_screenshot(animation["screenshot"]),
                (OPTIONS_SCREENSHOT_SIZE, OPTIONS_SCREENSHOT_SIZE),
            )

    def calculate_animations_rectangles(self):
        margin = OPTIONS_BOX_MARGIN
        box_size = OPTIONS_SCREENSHOT_SIZE
        start_x = (
            SCREEN_WIDTH
            - (self.options_columns * box_size + (self.options_columns - 1) * margin)
        ) // 2
        start_y = OPTIONS_OFFSET_Y
        for i, animation_option in enumerate(self.animations_options):
            col = i % self.options_columns
            row = i // self.options_columns
            x = start_x + col * (box_size + margin)
            y = start_y + row * (box_size + margin)

            rect = pygame.Rect(x, y, box_size, box_size + OPTIONS_FONT_SIZE)
            animation_option["rect"] = rect

    def render_animiations_options(self):
        for animation_option in self.animations_options:
            rect: pygame.Rect = animation_option["rect"]

            pygame.draw.rect(
                self.screen,
                SECOND_BACKGROUND_COLOR,
                rect,
            )
            self.screen.blit(animation_option["image"], (rect.x, rect.y))

            title_surface = self.option_font.render(
                animation_option["title"], True, TEXT_COLOR
            )
            title_rect = title_surface.get_rect(
                center=(
                    rect.x + rect.width // 2,
                    rect.y + rect.height - OPTIONS_FONT_SIZE / 2,
                )
            )
            self.screen.blit(title_surface, title_rect)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_title()
        self.render_animiations_options()

    def handle_click(self, position):
        for animation in self.animations_options:
            rect: pygame.Rect = animation["rect"]
            if rect.collidepoint(position):
                animation_title = animation["title"]
                print(f"clicked od animation {animation_title}")


pygame.init()
clock = pygame.time.Clock()
menu = MainMenu()
menu.draw()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            menu.handle_click(pygame.mouse.get_pos())
