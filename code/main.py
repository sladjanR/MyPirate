from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join    # Gives relative paths to specific os

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WIDNDOW_HEIGHT))
        pygame.display.set_caption("My Pirate World")
        # Cap fps (not to go 1000, and not to be too low for slow PC-s)
        self.clock = pygame.time.Clock()

        self.tmx_maps = {0: load_pygame(join('data','levels','omni.tmx'))}

        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        while True:
            # Divsion  with 1000 seconds
            # in a .tick() method we pass how much fps we want, if are no arguments there it's maximum frame rate for us
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()