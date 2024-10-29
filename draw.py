import pygame

class Draw:

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def draw_score(self, score: int, streak: int) -> None:
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        streak_text = font.render(f'Streak: {streak}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(streak_text, (10, 50))

    def draw_board(self, left_pos: int, right_pos: int, screen: pygame.Surface, screen_height: int) -> None:
        pygame.draw.rect(screen, (255, 255, 255), (left_pos - 50, 0, 5, screen_height))
        pygame.draw.rect(screen, (255, 255, 255), (right_pos + 50, 0, 5, screen_height))

    def draw_choose_difficulty(self, screen_width: int, screen_height: int, chosen: int = 0) -> None:
        big_font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        colors = {
            0: [255, 255, 255],
            1: [255, 255, 255],
            2: [255, 255, 255],
        }

        colors[chosen] = [255, 255, 0]

        easy_text = big_font.render('Easy', True, colors[0])
        medium_text = big_font.render('Medium', True, colors[1])
        hard_text = big_font.render('Hard', True, colors[2])
        bottom_text = small_font.render('Press Enter to continue', True, (255, 255, 255))


        middle_screen_height = screen_height // 2
        middle_screen_width = screen_width // 2

        easy_text_rect = easy_text.get_rect(center=(middle_screen_width, middle_screen_height - 50))
        medium_text_rect = medium_text.get_rect(center=(middle_screen_width, middle_screen_height))
        hard_text_rect = hard_text.get_rect(center=(middle_screen_width, middle_screen_height + 50))
        bottom_text_rect = bottom_text.get_rect(center=(middle_screen_width, middle_screen_height + 100))

        self.screen.blit(easy_text, easy_text_rect)
        self.screen.blit(medium_text, medium_text_rect)
        self.screen.blit(hard_text, hard_text_rect)
        self.screen.blit(bottom_text, bottom_text_rect)