import pygame

class DebugHUD:
    def __init__(self, font):
        self.font = font

    def draw_player_states(self, screen, player):
        y = 10
        x = 10
        
        # List all states to display
        lines = [
            f"Position: {int(player.rect.x)}, {int(player.rect.y)}",
            f"Velocity: {round(player.physic_handler.velocity.x,2)}, {round(player.physic_handler.velocity.y,2)}",
            f"On Ground: {player.onGround}",
            f"wishJump: {player.movement['jump']}",
            f"wishDash: {player.movement['dash']}",
            f"wishSlide: {player.movement['slide']}",
            f"Left: {player.movement['left']}",
            f"Right: {player.movement['right']}",
            f"State: {player.physic_handler.state}"
        ]

        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (x, y))
            y += 25  # space between lines