import pygame
from Modules.PlayerModules.PlayerController import Player

class EntityHandler:
    def __init__(self, screen_width, screen_height, player_img, size):
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Spawn player here
        self.player = Player("Player",
                             player_img,
                             (screen_width // 2, screen_height // 2),
                             size)

        self.all_sprites.add(self.player)
        self.players.add(self.player)

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update(self, dt):
        self.all_sprites.update(dt)

        # Handle world collisions, detection etc
        self.handle_world_collision()

    def handle_world_collision(self):
        """Very simple example: ground collision."""
        floor_y = 720 - 100
        wall_xl = 1280 - 50
        wall_xr = 50

        if self.player.rect.bottom >= floor_y:
            self.player.rect.bottom = floor_y
            self.player.onGround = True
        else:
            self.player.onGround = False

        if self.player.rect.left <= wall_xr:
            self.player.rect.left = wall_xr
            if self.player.physic_handler.velocity.x < 0:
                self.player.physic_handler.velocity.x = 0
        elif self.player.rect.right >= wall_xl:
            self.player.rect.right = wall_xl
            if self.player.physic_handler.velocity.x > 0:
                self.player.physic_handler.velocity.x = 0

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self, screen):
        self.all_sprites.draw(screen)