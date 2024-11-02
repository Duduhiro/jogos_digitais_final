from __future__ import annotations

import random
import pygame
from typing import Optional

from entities import Arrow
from draw import Draw
from score import Score

ARROW_TYPES = {
    'left':      {'rotation': 270, 'color': (255, 0, 0), 'key': pygame.K_LEFT},
    'right':     {'rotation': 90, 'color': (64, 0, 128), 'key': pygame.K_RIGHT},
    'up':        {'rotation': 180, 'color': (0, 0, 255), 'key': pygame.K_UP},
    'down':      {'rotation': 0, 'color': (0, 0, 0), 'key': pygame.K_DOWN},
}

# Class for controlling the game logic
class Engine:

    def __init__(self, screen: pygame.Surface, screen_width: int, screen_height: int) -> None:
        self.screen = screen
        self.base_arrows = pygame.sprite.Group()
        self.moving_arrows = pygame.sprite.Group()
        self.draw_screen = Draw(self.screen)
        self.score = Score()

        self.difficulty = 0
        self.falling_speed = 0
        self.last_spawn = 0

        self.arrow_spawn_pos = {
            'left':  screen_width // 2 - 120,
            'up':    screen_width // 2 - 40,
            'down':  screen_width // 2 + 40,
            'right': screen_width // 2 + 120
        }
        self.arrow_spawn_delay = [
            1000,
            800,
            600
        ]
        self.arrow_per_level = [
            10,
            15,
            20
        ]
        self.count_arrows = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    def reset_game(self) -> None:
        self.score.reset()
        self.moving_arrows.empty()
        self.count_arrows = 0

    def create_base_arrow(self) -> None:
        
        spawn_height = self.screen_height - 150
        
        for direction, props in ARROW_TYPES.items():
            x_position = self.arrow_spawn_pos[direction]
            arrow = Arrow(
                x=x_position,
                y=spawn_height,
                rotation=props['rotation'],
                color=props['color'],
                key=props['key']
            )
            self.base_arrows.add(arrow)

    def update(self) -> bool:
        
        # Update the entire game
        # Spawn the falling arrows
        self.spawn_arrows()

        # Update all the moving arrows
        for arrow in self.moving_arrows:

            # Update the position of the arrow and if the player hit the arrow, return its Y position for scoring           
            y_pos = arrow.update(self.falling_speed, self.screen_height)
            
            # If the previous function return a value, calculate the score according to the position of the arrow
            if y_pos is not None:
                
                # If the arrow is within 10 pixels of the bottom arrows, give 100 points
                self.calculate_score(y_pos)
                self.count_arrows += 1

        # Update the score screen
        self.draw_screen.draw_score(self.score.score, self.score.streak)

        return self.count_arrows >= self.arrow_per_level[self.difficulty]

    def calculate_score(self, y_pos: int) -> None:
        if self.screen_height - 150 -10 < y_pos < self.screen_height - 150 + 10:
            self.score.update_score(100)
            self.score.update_streak(True)
        elif (self.screen_height - 150 - 20) <= y_pos < (self.screen_height - 150 - 10) or (self.screen_height - 150 + 10) < y_pos <= (self.screen_height - 150 + 20):
            self.score.update_score(50)
            self.score.update_streak(True)
        else:
            self.score.update_streak(False)

    def draw(self) -> None:
        
        # Draw the entire game
        self.base_arrows.draw(self.screen)
        self.moving_arrows.draw(self.screen)
        self.draw_screen.draw_board(self.arrow_spawn_pos['left'], self.arrow_spawn_pos['right'], self.screen_height)

    def spawn_arrows(self) -> None:
        
        # Spawn the falling arrows
        # This part check if the time since the last arrow spawned is greater than the delay for the current difficulty
        current_time = pygame.time.get_ticks()

        if current_time - self.last_spawn < self.arrow_spawn_delay[self.difficulty]:
            return
        self.last_spawn = current_time

        # Choose a random position to spawn the arrow
        chosen_arrow = random.choice(list(ARROW_TYPES.keys()))
        arrow_props = ARROW_TYPES[chosen_arrow] 
        x_position = self.arrow_spawn_pos[chosen_arrow]
        
        arrow = Arrow(
            x=x_position,
            rotation=arrow_props['rotation'],
            color=arrow_props['color'],
            key=arrow_props['key']
        )

        self.moving_arrows.add(arrow)

    def main_menu(self, clock: pygame.time.Clock) -> bool:

        diff = 0
        # Function to select the difficulty of the game
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    diff = (diff - 1) % 3
                elif keys[pygame.K_DOWN]:
                    diff = (diff + 1) % 3
                elif keys[pygame.K_RETURN]:
                    self.difficulty = diff
                    self.falling_speed = (diff + 1) * 2 + 1
                    return True

            self.screen.fill((0, 0, 0))
            self.draw_screen.draw_choose_difficulty(self.screen_height, diff)
            pygame.display.flip()
            clock.tick(60)

    def main_game(self, clock: pygame.time.Clock) -> bool:

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    resume = self.pause_game(clock)

                    if resume is not None:
                        return resume
            
            self.screen.fill((0, 0, 0))

            if self.update():
                return True
            self.draw()

            pygame.display.flip()
            clock.tick(60)

    def pause_game(self, clock: pygame.time.Clock) -> Optional[bool]:

        option = 0
        starting_time = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    option = (option - 1) % 2
                elif keys[pygame.K_DOWN]:
                    option = (option + 1) % 2
                elif keys[pygame.K_RETURN]:
                    if option == 0:
                        end_time = pygame.time.get_ticks()
                        self.last_spawn += end_time - starting_time
                        return 
                    elif option == 1:
                        return True

            self.screen.fill((0, 0, 0))
            self.draw_screen.draw_pause_screen(self.screen_height, option)

            pygame.display.flip()
            clock.tick(60)

    def end_game(self, clock: pygame.time.Clock) -> bool:

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.reset_game()
                    return True

            self.screen.fill((0, 0, 0))
            self.draw_screen.draw_end_screen(self.screen_height, self.score.score, self.arrow_per_level[self.difficulty] * 100, self.score.max_streak)

            pygame.display.flip()
            clock.tick(60)