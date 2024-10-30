from __future__ import annotations

import random
import pygame
from typing import Optional

from entities import LeftArrow, RightArrow, UpArrow, DownArrow
from draw import Draw
from score import Score

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
            20,
            10 # TEMP
        ]
        self.count_arrows = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

    def reset_game(self) -> None:
        self.score.reset()
        self.moving_arrows.empty()
        self.count_arrows = 0

    def create_base_arrow(self) -> None:
        
        # Create the arrows in the bottom of the screen
        lArrow = LeftArrow(self.arrow_spawn_pos['left'], self.screen_height - 150)
        self.base_arrows.add(lArrow)
        
        uArrow = UpArrow(self.arrow_spawn_pos['up'], self.screen_height - 150)
        self.base_arrows.add(uArrow)

        dArrow = DownArrow(self.arrow_spawn_pos['down'], self.screen_height - 150)
        self.base_arrows.add(dArrow)

        rArrow = RightArrow(self.arrow_spawn_pos['right'], self.screen_height - 150)
        self.base_arrows.add(rArrow)

    def update(self) -> None:
        
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
                if self.screen_height - 150 - 10 < y_pos < self.screen_height - 150 + 10:
                    self.score.update_score(100)
                    self.score.update_streak(True)

                # If the arrow is within 20 pixels of the bottom arrows, give 50 points
                elif (self.screen_height - 150 - 20 <= y_pos <= self.screen_height - 150 - 10) or (self.screen_height - 150 + 10 <= y_pos <= self.screen_height - 150 + 20):
                    self.score.update_score(50)
                    self.score.update_streak(True)
                
                # Reset the streak if the player pressed to late, early or didn't press at all
                else:
                    self.score.update_streak(False)

                self.count_arrows += 1

        # Update the score screen
        self.draw_screen.draw_score(self.score.score, self.score.streak)

        return self.count_arrows >= self.arrow_per_level[self.difficulty]

    def draw(self) -> None:
        
        # Draw the entire game
        self.base_arrows.draw(self.screen)
        self.moving_arrows.draw(self.screen)
        self.draw_screen.draw_board(self.arrow_spawn_pos['left'], self.arrow_spawn_pos['right'], self.screen, self.screen_height)

    def spawn_arrows(self) -> None:
        
        # Spawn the falling arrows
        
        # This part check if the time since the last arrow spawned is greater than the delay for the current difficulty
        current_time = pygame.time.get_ticks()

        if current_time - self.last_spawn < self.arrow_spawn_delay[self.difficulty]:
            return
        self.last_spawn = current_time

        # Choose a random position to spawn the arrow
        chosen_arrow = random.choice(['left', 'up', 'down', 'right'])
        
        if chosen_arrow == 'left':
            arrow = LeftArrow(self.arrow_spawn_pos[chosen_arrow])
        elif chosen_arrow == 'up':
            arrow = UpArrow(self.arrow_spawn_pos[chosen_arrow])
        elif chosen_arrow == 'down':
            arrow = DownArrow(self.arrow_spawn_pos[chosen_arrow])
        elif chosen_arrow == 'right':
            arrow = RightArrow(self.arrow_spawn_pos[chosen_arrow])

        self.moving_arrows.add(arrow)

    def main_menu(self, clock: pygame.time.Clock) -> bool:

        diff = 0

        # Function to the player choose to start the game
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    if diff > 0:
                        diff -= 1
                    else:
                        diff = 2

                elif keys[pygame.K_DOWN]:
                    if diff < 2:
                        diff += 1
                    else:
                        diff = 0

                elif keys[pygame.K_RETURN]:
                    self.difficulty = diff
                    self.falling_speed = (diff + 1) * 2 + 1
                    return True

            self.screen.fill((0, 0, 0))
            self.draw_screen.draw_choose_difficulty(self.screen_width, self.screen_height, diff)

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

            check_end = self.update()
            if check_end:
                return True

            self.draw()

            pygame.display.flip()

            clock.tick(60)

    def pause_game(self, clock: pygame.time.Clock) -> Optional[bool]:

        option = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    if option > 0:
                        option -= 1
                    else:
                        option = 1

                elif keys[pygame.K_DOWN]:
                    if option < 1:
                        option += 1
                    else:
                        option = 0

                elif keys[pygame.K_RETURN]:
                    if option == 0:
                        return 

                    elif option == 1:
                        return True

            self.screen.fill((0, 0, 0))
            self.draw_screen.draw_pause_screen(self.screen_width, self.screen_height, option)

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
            self.draw_screen.draw_end_screen(self.screen_width, self.screen_height, self.score.score, self.score.max_streak)

            pygame.display.flip()
            clock.tick(60)