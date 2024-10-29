import pygame

from typing import Optional

HIT_BOX = 100

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int = 0, rotation: int = 0, color: tuple = (False, (0, 0, 0))):
        super().__init__()

        self.image = pygame.image.load('arrow.png')
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.scale(self.image, (50, 50))
        if color[0]:
            self.image.fill(color[1], special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

    def update(self, speed: int = 0, screen_height: int = 0, arrow_key: int = None) -> Optional[int]:
        self.rect.centery += speed
        
        # If the arrow is out of the screen, kill it
        if self.rect.centery > screen_height - 30 and speed > 0:
            self.kill()
            return -1
        
        # If the player press the arrow key and the arrow is within the hit box, return the Y position of the arrow
        keys = pygame.key.get_pressed()
        if keys[arrow_key] and speed > 0 and abs(self.rect.centery - (screen_height - 150)) < HIT_BOX:
            y = self.rect.centery
            self.kill()
            return y
            
class LeftArrow(Arrow):
    def __init__(self, x: int, y: int = 0):
        super().__init__(x, y, 270, (True, (255, 0, 0)))

    def update(self, speed: int = 0, screen_height: int = 0) -> Optional[int]:
        return super().update(speed, screen_height, pygame.K_LEFT)


class RightArrow(Arrow):
    def __init__(self, x: int, y: int = 0):
        super().__init__(x, y, 90, (True, (64, 0, 128)))

    def update(self, speed: int = 0, screen_height: int = 0) -> Optional[int]:
        return super().update(speed, screen_height, pygame.K_RIGHT)


class UpArrow(Arrow):
    def __init__(self, x: int, y: int = 0):
        super().__init__(x, y, 180, (True, (0, 0, 255)))

    def update(self, speed: int = 0, screen_height: int = 0) -> Optional[int]:
        return super().update(speed, screen_height, pygame.K_UP)


class DownArrow(Arrow):
    def __init__(self, x: int, y: int = 0):
        super().__init__(x, y)

    def update(self, speed: int = 0, screen_height: int = 0) -> Optional[int]:
        return super().update(speed, screen_height, pygame.K_DOWN)