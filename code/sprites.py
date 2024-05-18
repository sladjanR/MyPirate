from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) # One is for width, second is for height
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft = pos) # Creates floating point rect
        self.old_rect = self.rect.copy()
