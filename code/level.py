from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map):
        # We want to target one specific layer

        # x, y - is not pixel positions, it is positions in a grid, because of that we have * TILE_SIZE
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites)
        # print(tmx_map)

        for obj in tmx_map.get_layer_by_name('Objects'):
            #print(obj)
            if obj.name == "player":
                # With obj we gets original positions do not need to multiply with TILE_SIZE
                Player((obj.x, obj.y), self.all_sprites)
                # print(obj.x)
                # print(obj.y)
            

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
        