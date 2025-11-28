import pygame
import random

WIDTH, HEIGHT, FPS = 1280, 720, 60

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Screen")

clock = pygame.time.Clock()

# class PlayerController:

player_img = pygame.image.load("C:\\Users\\Drawi\\Documents\\QuickProject\\scr\\assets\\img\\char\\Arrow.png").convert_alpha()
class Player(pygame.sprite.Sprite):
    
    def __init__(self, name):
        super().__init__()

        # Attributes
        self.name = name
        self.baseHp = 10
        self.baseStam = 3
        self.baseSpeed = 5

        # Sprite init
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Movement
        self.movement = {
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0  
        self.turn_speed = 12  

    def inputHandler(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movement["left"] = True
                if event.key == pygame.K_d:
                    self.movement["right"] = True
                if event.key == pygame.K_w:
                    self.movement["up"] = True
                if event.key == pygame.K_s:
                    self.movement["down"] = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement["left"] = False
                if event.key == pygame.K_d:
                    self.movement["right"] = False
                if event.key == pygame.K_w:
                    self.movement["up"] = False
                if event.key == pygame.K_s:
                    self.movement["down"] = False

    # def update(self, deltatime):
    #     wishdir = pygame.math.Vector2(0, 0)
    #     target_velocity = pygame.math.Vector2(0, 0)

    #     if self.movement["up"]:
    #         wishdir.y = -1
    #     if self.movement["down"]:
    #         wishdir.y = 1
    #     if self.movement["left"]:
    #         wishdir.x = -1
    #     if self.movement["right"]:
    #         wishdir.x = 1

    #     accel = 20
    #     friction = 10
        
    #     if wishdir.length_squared() != 0:
    #         wishdir = wishdir.normalize()
    #         self.velocity += wishdir * accel * dt

    #         # speed clamp
    #         if self.velocity.length() > self.baseSpeed:
    #             self.velocity.scale_to_length(self.baseSpeed)
    #     else:
    #         speed = self.velocity.length()
    #         new_speed = max(0, speed - friction * dt)

    #         if new_speed == 0:
    #             self.velocity.xy = (0, 0)
    #         else:
    #             self.velocity.scale_to_length(new_speed)
            
    #     deadzone = 0.05
    #     if abs(self.velocity.x) < deadzone:
    #         self.velocity.x = 0
    #     if abs(self.velocity.y) < deadzone:
    #         self.velocity.y = 0

        
    #     # Update 
    #     self.rect.center += self.velocity * deltatime * 60

    def smooth_rotate(self, target_angle, dt):

        diff = (target_angle - self.rotation + 180) % 360 - 180

        self.rotation += diff * min(1, self.turn_speed * dt)

    def update(self, dt):

        wishdir = pygame.math.Vector2(
            (self.movement["right"] - self.movement["left"]),
            (self.movement["down"] - self.movement["up"])
        )

        wishspeed = self.baseSpeed 

        if wishdir.length_squared() > 0:
            wishdir = wishdir.normalize()
        else:
            wishdir = pygame.math.Vector2()

        speed = self.velocity.length()

        if speed != 0:
            drop = 0

            friction = 2  
            control = max(speed, 10)
            drop += control * friction * dt

            new_speed = max(0, speed - drop)

            if new_speed != speed:
                self.velocity.scale_to_length(new_speed) if new_speed > 0 else self.velocity.update(0, 0)


        if wishdir.length_squared() > 0:
            accel = 40 
            
            currentspeed = self.velocity.dot(wishdir)

            addspeed = wishspeed - currentspeed
            if addspeed > 0:
                accelspeed = accel * dt * wishspeed
                if accelspeed > addspeed:
                    accelspeed = addspeed
                self.velocity += wishdir * accelspeed

        self.rect.center += self.velocity * dt * 60
                
        if self.velocity.length_squared() > 0:
                 
            target_angle = self.velocity.angle_to(pygame.math.Vector2(-1, 0))

            self.smooth_rotate(target_angle, dt)

            base_img = pygame.transform.scale(player_img, (50, 50))
            self.image = pygame.transform.rotate(base_img, self.rotation)

            self.rect = self.image.get_rect(center=self.rect.center)

player = Player("Player")
all_sprites = pygame.sprite.Group(player)


running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            running = False 
        player.inputHandler(Event)  # update movement dict
        
    all_sprites.update(dt)
    
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
