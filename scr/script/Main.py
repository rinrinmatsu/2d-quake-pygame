import pygame

from Modules.EntitiesHandler.EntitiesHandler import EntityHandler 
from Modules.UiHandler.Debug import DebugHUD

SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS = 1280, 720, 60

floor_y = SCREEN_HEIGHT - 100

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("silkscreen", 20)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Scroll")
clock = pygame.time.Clock()

player_img = pygame.image.load("assets/img/entities/Arrow.png").convert_alpha()

entities = EntityHandler(SCREEN_WIDTH, SCREEN_HEIGHT, player_img, (30, 30))
debug_hud = DebugHUD(font)

running = True
while running:
    dt = clock.tick(SCREEN_FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        entities.player.inputHandler(event)  
        
    entities.update(dt)
    
    screen.fill((30, 30, 30))
    entities.draw(screen)
    debug_hud.draw_player_states(screen, entities.player)
    pygame.display.flip()
            
pygame.quit() 