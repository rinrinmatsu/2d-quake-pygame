import pygame

from .Handlers.PhysicHandler import PhysicHandler

class Player(pygame.sprite.Sprite):
    def __init__(self, name, player_img, pos, size):
        super().__init__()
        
        # attributes
        self.name = name
        
        self.onGround = False
        self.facing_right = True
        
        #sprite init
        self.image = pygame.transform.scale(player_img, size)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        
        #movement
        self.physic_handler = PhysicHandler(self)
        
        self.movement = {
            "left": False,
            "right": False,
            "jump": False,
            "crouch": False,
            "dash": False,
            "slide": False
        }
        
    def inputHandler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.movement["left"] = True
            if event.key == pygame.K_d:
                self.movement["right"] = True
            if event.key == pygame.K_w:
                self.movement["jump"] = True
            if event.key == pygame.K_s:
                self.movement["crouch"] = True
            if event.key == pygame.K_LSHIFT:
                self.movement["dash"] = True
            if event.key == pygame.K_LCTRL:
                self.movement["slide"] = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.movement["left"] = False
            if event.key == pygame.K_d:
                self.movement["right"] = False
            if event.key == pygame.K_w:
                self.movement["jump"] = False
            if event.key == pygame.K_s:
                self.movement["crouch"] = False
            if event.key == pygame.K_LSHIFT:
                self.movement["dash"] = False
            if event.key == pygame.K_LCTRL:
                self.movement["slide"] = False
                
    def flipSprite(self, camera_offset_x: int = 0):
        mx, my = pygame.mouse.get_pos()
        if mx > self.rect.centerx + camera_offset_x:
            self.facing_right = True
        elif mx < self.rect.centerx + camera_offset_x:
            self.facing_right = False
            
        if self.facing_right:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)
                    
    def update(self, dt):
        self.flipSprite()
        self.physic_handler.update(dt)
        
        
        