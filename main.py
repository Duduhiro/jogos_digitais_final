import pygame

from engine import Engine

def main() -> None:

    pygame.init()

    SCREEN_RES = (800, 600)

    screen = pygame.display.set_mode(SCREEN_RES)
    pygame.display.set_caption('Dance it!')
    clock = pygame.time.Clock()

    running = True

    engine = Engine(screen, *SCREEN_RES)
    engine.create_base_arrow()

    while running:
        
        # Render the main menu
        start = engine.main_menu(clock)
        if not start:
            return

        # Render the game
        cont = engine.main_game(clock)
        if not cont:
            return

        # Render the end game
        restart = engine.end_game(clock)
        if not restart:
            return


if __name__ == '__main__':
    main()