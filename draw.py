import pygame

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BIG_FONT_SIZE = 36
SMALL_FONT_SIZE = 24

class Draw:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def render_text(self, text: str, font_size: int, color: tuple) -> pygame.Surface:
        font = pygame.font.Font(None, font_size)
        return font.render(text, True, color)

    def draw_centered_text(self, text: str, y_pos: int, font_size: int, color: tuple) -> None:
        text_surface = self.render_text(text, font_size, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_pos))
        self.screen.blit(text_surface, text_rect)

    def draw_score(self, score: int, streak: int) -> None:
        
        font = pygame.font.Font(None, BIG_FONT_SIZE)

        score_text = font.render(f"Score: {score}", True, WHITE)
        streak_text = font.render(f"Streak: {streak}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(streak_text, (10, 50))

    def draw_board(self, left_pos: int, right_pos: int, screen_height: int) -> None:
        pygame.draw.rect(self.screen, WHITE, (left_pos - 50, 0, 5, screen_height))
        pygame.draw.rect(self.screen, WHITE, (right_pos + 50, 0, 5, screen_height))

    def draw_choose_difficulty(self, screen_height: int, chosen: int = 0) -> None:
        colors ={0: WHITE, 1: WHITE, 2: WHITE}

        colors[chosen] = YELLOW

        middle_screen_height = screen_height // 2

        self.draw_centered_text("Choose difficulty", middle_screen_height - 50, BIG_FONT_SIZE, WHITE)
        self.draw_centered_text("Easy", middle_screen_height, BIG_FONT_SIZE, colors[0])
        self.draw_centered_text("Medium", middle_screen_height + 50, BIG_FONT_SIZE, colors[1])
        self.draw_centered_text("Hard", middle_screen_height + 100, BIG_FONT_SIZE, colors[2])

    def draw_end_screen(self, screen_height: int, score: int, max_score: int, max_streak: int) -> None:

        middle_screen_height = screen_height // 2

        self.draw_centered_text("Game Over", middle_screen_height - 50, BIG_FONT_SIZE, WHITE)
        self.draw_centered_text(f"Score: {score}/{max_score}", middle_screen_height, BIG_FONT_SIZE, WHITE)
        self.draw_centered_text(f"Max streak: {max_streak}", middle_screen_height + 50, BIG_FONT_SIZE, WHITE)
        self.draw_centered_text("Press ENTER to restart", middle_screen_height + 100, SMALL_FONT_SIZE, WHITE)

    def draw_pause_screen(self, screen_width: int, chosen: int) -> None:

        colors = {0: WHITE, 1: WHITE}

        colors[chosen] = YELLOW

        middle_screen_width = screen_width // 2

        self.draw_centered_text("Game Paused", middle_screen_width - 50, BIG_FONT_SIZE, WHITE)
        self.draw_centered_text("Resume", middle_screen_width, BIG_FONT_SIZE, colors[0])
        self.draw_centered_text("Restart", middle_screen_width + 50, BIG_FONT_SIZE, colors[1])