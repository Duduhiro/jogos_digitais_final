import pygame
from typing import Optional

HIT_BOX = 100
ARROW_SIZE = (50, 50)
ARROW_IMAGE_PATH = 'arrow.png'


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int = 0, rotation: int = 0, color: tuple = (0, 0, 0), key: int = None):
        super().__init__()
        
        # Load the arrow image, rotate it, scale it and color it
        self.image = pygame.image.load(ARROW_IMAGE_PATH)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.scale(self.image, ARROW_SIZE)
        if color != (0, 0, 0):
            self.image.fill(color, special_flags=pygame.BLEND_ADD)

        # Get the rectangle of the arrow and set its position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Set the key of the arrow
        self.key = key

    def update(self, speed: int = 0, screen_height: int = 0) -> Optional[int]:
        # Move the arrow down
        self.rect.centery += speed
        
        # If the arrow is out of the screen, kill it
        if self.rect.centery > screen_height - 30 and speed > 0:
            self.kill()
            return -1
        
        # If the player press the arrow key and the arrow is within the hit box, return the Y position of the arrow
        keys = pygame.key.get_pressed()
        if keys[self.key] and speed > 0 and abs(self.rect.centery - (screen_height - 150)) < HIT_BOX:
            y = self.rect.centery
            self.kill()
            return y
            