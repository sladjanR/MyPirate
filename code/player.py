from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill("orange")

        # Rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        #------------------------
        # Movement
        # We can get vector because we import that from settings
        self.direction = vector(0,0)
        self.speed = 200    # Before we added data time (dt) it was 0.2
        self.gravity = 700 # Because fall speed is not the same with speed of x, so we created another variable
        self.jump = False
        self.jump_heigt = 500

        #---------------------------
        # Collision
        self.collision_sprites = collision_sprites
        # print(self.collision_sprites) -> To see how big is our group of sprites

        # We want to know is player on surface, and if he is, then he can again jump
        self.on_surface = {"floor" : False, "left" : False, "right": False}


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
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x  # normalize() -> We want to be sure that length is ALWAYS 1
        # Above we are used thernal operator because we cant normalize if vector have no elements
        # We added later to normalize only x (horizontal), but for y we want to be more than 1 (be faster)

        if keys[pygame.K_SPACE]:
            # self.direction.y = -100 -> This can be feature :)
            self.jump = True

    def move(self, dt):
        # horizontal
        #self.rect.topleft += self.direction * self.speed * dt -> That was it look before
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        

        # vertical
        # If we fall longer it be faster, because of that we use Data Time (dt)
        # Also we want to fall be frame independent, if framerate changes not change behavior (because of that we divide by 2 and use two times)
        self.direction.y += self.gravity / 2  * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2  * dt
        self.collision("vertical")

        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_heigt
            
            # Be sure that is out of inside if 
            self.jump = False
            
    
    def check_contact(self):
        # We want to create a cuple of small rectangles around our player 1.08
        floor_rect = pygame.Rect((self.rect.bottomleft,),(self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # collisions
        self.on_surface["floor"] = True if floor_rect.collidelist(collide_rects) >= 0 else False


        #TODO:
        # Improve this that direction.y not goes no infinity :), it uses so much memory (of course we set that to 0 when is collision)
        # but what if we stay in one position so much time ;)


    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "horizontal":
                    # Left collision -> but this isn't enought
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:

                        self.rect.left = sprite.rect.right

                    # Right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                else: # Vertical collision
                    if self.rect.top <=  sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    
                    self.direction.y = 0

    # Override
    def update(self, dt):
        self.old_rect = self.rect.copy()    # Our old position before collision, to now from which side is collision, where is player before
        self.input()
        self.move(dt)
        self.check_contact()