from settings import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites):
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
        self.semi_collision_sprites = semi_collision_sprites
        # print(self.collision_sprites) -> To see how big is our group of sprites

        # We want to know is player on surface, and if he is, then he can again jump
        self.on_surface = {"floor" : False, "left" : False, "right": False}
        self.platform = None

        # timer
        self.timers= {
            "wall jump" : Timer(350),
            "wall slide block" : Timer(250),
            "platform skip" : Timer(300)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        if not self.timers["wall jump"].active:
            if keys[pygame.K_RIGHT]:
                # print("Right")
                input_vector.x += 1
            if keys[pygame.K_LEFT]:
                # print("Left")
                input_vector.x -= 1
            if keys[pygame.K_DOWN]:
                self.timers["platform skip"].activate()
            
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


        if not self.on_surface["floor"] and any((self.on_surface["left"], self.on_surface["right"])) and not self.timers["wall slide block"].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt

        else:
            self.direction.y += self.gravity / 2  * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2  * dt


        # TODO: (srpski): OVAJ self.collision mi pravi problem, treba da je postavljen posle self.jump upita, ali jedino ovako radi
        self.collision("vertical")
        self.semi_collision()

        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_heigt
                self.timers["wall slide block"].activate()
                self.rect.bottom -= 1   # Player is not glued to the platform
            elif any((self.on_surface["left"], self.on_surface["right"])) and not self.timers["wall slide block"].active:  # Once player is on wall, and we try to jump, we activate timer and not allow any left and right input
                self.timers["wall jump"].activate()     # To block two inputs (left and right)
                self.direction.y = -self.jump_heigt
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False

        
    def platform_move(self, dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt       # We want to our player moves with platform with same speed and direction
    
    def check_contact(self):
        # We want to create a cuple of small rectangles around our player 1.08
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width, 2))
        # Wall collision left and right 1.13
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft  + vector(-2, self.rect.height / 4), (2, self.rect.height / 2))

        # To see if it works
        # pygame.draw.rect(self.display_surface, "yellow", floor_rect)
        # pygame.draw.rect(self.display_surface, "yellow", right_rect)
        # pygame.draw.rect(self.display_surface, "yellow", left_rect)

        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        # collisions
        self.on_surface["floor"] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >=0 else False
        self.on_surface["right"] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface["left"]  = True if left_rect.collidelist(collide_rects)   >= 0 else False
        # print(self.on_surface)

        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite


        #TODO:
        # Improve this that direction.y not goes no infinity :), it uses so much memory (of course we set that to 0 when is collision)
        # but what if we stay in one position so much time ;)


    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):      
                if axis == "horizontal":
                    # Left collision -> but this isn't enought
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= sprite.old_rect.right:     # All old_rects in the int() function

                        self.rect.left = sprite.rect.right

                    # Right collision
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                else: # Vertical collision
                    # Top
                    if self.rect.top <=  sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        if hasattr(sprite, "moving"):
                            self.rect.top += 6  # Fix bug when moving platform goes down, and player jumps, then player stucking in the middle of platform
                                                # You can TODO add timer to disable collison for the better feeling
                    # Bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    
                    self.direction.y = 0

    def semi_collision(self):
        if not self.timers["platform skip"].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:     # Added later to be in int()
                        self.rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    # Override
    def update(self, dt):
        self.old_rect = self.rect.copy()    # Our old position before collision, to now from which side is collision, where is player before
        self.update_timers()
        self.input()
        self.move(dt)
        self.platform_move(dt)
        self.check_contact()
        # print(self.timers["wall jump"].active)