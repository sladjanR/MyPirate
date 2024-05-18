from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill("orange")
        self.rect = self.image.get_frect(topleft = pos)

        #------------------------
        # Movement
        # We can get vector because we import that from settings
        self.direction = vector(0,0)
        self.speed = 200    # Before we added data time (dt) it was 0.2


    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        if keys[pygame.K_RIGHT]:
            # print("Right")
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            # print("Left")
            input_vector.x -= 1
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
        self.direction = input_vector.normalize() if input_vector else input_vector  # normalize() -> We want to be sure that length is ALWAYS 1
        # Above we are used thernal operator because we cant normalize if vector have no elements

    def move(self, dt):
        self.rect.topleft += self.direction * self.speed * dt

    # Override
    def update(self, dt):
        self.input()
        self.move(dt)