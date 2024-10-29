import pygame

from engine import Engine

def main() -> None:

    pygame.init()

    SCREEN_RES = (800, 600)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Dance it!')
    clock = pygame.time.Clock()

    running = True

    engine = Engine(screen, *SCREEN_RES)

    engine.create_base_arrow()

    cont = engine.choose_difficulty(clock)

    if not cont:
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))

        engine.update()
        engine.draw()

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()