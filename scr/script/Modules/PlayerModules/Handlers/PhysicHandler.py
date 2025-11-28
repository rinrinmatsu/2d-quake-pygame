# import pygame
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from PlayerController import Player

# class PhysicHandler:
#     def __init__(self, player: 'Player'):
#         self.player = player

#         self.baseSpeed = 10
#         self.backSpeed = 7
#         self.accel = 50
#         self.friction = 6

#         self.coyoteTime = 0.15
#         self.bufferTime = 0.1

#         self.gravity = 35
#         self.maxFallSpeed = 50
#         self.maxAirSpeed = 75

#         self.jumpPower = 15
#         self.maxJump = 2
#         self.jumpCount = 0
#         self.jumpCooldown = 0.2

#         self.maxStamina = 3
#         self.currentStamina = self.maxStamina
#         self.staminaRegenRate = 0.5
#         self.dashCost = 1
#         self.dashCooldown = 0.5
#         self.dashStrength = 50

#         self.onGround = player.onGround
#         self.wishDir = pygame.math.Vector2(0, 0)

#         self.wishJump = player.movement["jump"]
#         self.wishCrouch = player.movement["crouch"]
#         self.wishDash = player.movement["dash"]
#         self.wishSlide = player.movement["slide"]

#         self.currSpeed = 0
#         self.currDir = pygame.math.Vector2(0, 0)
#         self.velocity = pygame.math.Vector2(0, 0)

#     def state_update(self):
#         self.wishDir.x = 0
#         if self.player.movement["left"]:
#             self.wishDir.x -= 1
#         if self.player.movement["right"]:
#             self.wishDir.x += 1

#     def accel(self, wishdir, velocity, accel, dt):
#         if self.onGround:
#             wishspeed = abs(wishdir.x) * self.baseSpeed
#             addspeed = wishspeed - abs(velocity.x)
#             if addspeed > 0:
#                 accelspeed = accel * dt
#                 if accelspeed > addspeed:
#                     accelspeed = addspeed
#                 self.currSpeed += accelspeed * (1 if wishdir.x > 0 else -1)


#         elif not self.onGround:
#             velocity.y += self.gravity * dt
#             if velocity.y > self.maxFallSpeed:
#                 velocity.y = self.maxFallSpeed

#             if wishdir.x != 0 and wishdir.x :
#                 pass


#     def friction(self, velocity, friction, dt):
#         if self.onGround and  self.wishDir.x == 0:
#             speed = abs(velocity.x)
#             if speed != 0:
#                 drop = speed * friction * dt
#                 newSpeed = speed - drop
#                 if newSpeed < 0:
#                     newSpeed = 0
#                 velocity.x = newSpeed * (1 if velocity.x > 0 else -1)

#     def applyImpulse(self, velocity, impulseDir, impulseStrength):
#         velocity.x += impulseDir.x * impulseStrength
#         velocity.y += impulseDir.y * impulseStrength

#     def update(self, dt):
#         self.state_update()

#         self.player.rect.x += self.velocity.x
#         self.player.rect.y += self.velocity.y

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Modules.PlayerModules.PlayerController import Player

class PhysicHandler:
    def __init__(self, player: 'Player'):
        self.player = player
        self.sizeMultiplier = player.rect.size[1] / 10

        self.baseSpeed = 4 * self.sizeMultiplier
        self.accelRate = 15 * self.sizeMultiplier
        self.frictionRate = 5 * self.sizeMultiplier

        # Air
        self.gravity = 12 * self.sizeMultiplier
        self.maxFallSpeed = 15 * self.sizeMultiplier
        self.airAccel = 9 * self.sizeMultiplier
        self.airFriction = 0.4 * self.sizeMultiplier
        self.maxAirSpeed = 4 * self.sizeMultiplier

        # Jumps
        self.jumpPower = 5 * self.sizeMultiplier
        self.maxJump = 2
        self.jumpCount = 0
        self.jumpBufferTime = 0.12
        self.coyoteTime = 0.18

        # Timers
        self.jumpBufferTimer = 0
        self.coyoteTimer = 0
        self.jumpCooldown = 0.1
        self.jumpCDTimer = 0

        # Dash
        self.dashXStrength = 8 * self.sizeMultiplier
        self.dashYStrength = 1.5 * self.sizeMultiplier
        self.dashCooldown = 0.5
        self.dashTimer = 0
        self.canDash = True

        # Slide
        self.sliding = False
        self.slideDecay = 0.5 * self.sizeMultiplier

        # State
        self.velocity = pygame.math.Vector2(0, 0)
        self.wishDir = pygame.math.Vector2(0, 0)
        
        self.state = "idle"

    def update_wishdir(self):
        self.wishDir.x = 0
        if self.player.movement["left"]:
            self.wishDir.x -= 1
        if self.player.movement["right"]:
            self.wishDir.x += 1

    def accel_towards(self, target, rate, dt):
        diff = target - self.velocity.x
        step = rate * dt

        if abs(diff) <= step:
            self.velocity.x = target
        else:
            self.velocity.x += step * (1 if diff > 0 else -1)

    def apply_friction(self, rate, dt):
        if self.wishDir.x != 0:
            return

        if abs(self.velocity.x) <= 0.1:
            self.velocity.x = 0
            return

        self.velocity.x -= rate * dt * (1 if self.velocity.x > 0 else -1)

    # GROUND MOVEMENT
    def ground_move(self, dt):
        if self.wishDir.x != 0:
            target = self.wishDir.x * self.baseSpeed
            self.accel_towards(target, self.accelRate, dt)
        else:
            self.apply_friction(self.frictionRate, dt)
            self.state = "idle"

    # AIR MOVEMENT
    def air_move(self, dt):
        self.velocity.y += self.gravity * dt
        if self.velocity.y > self.maxFallSpeed:
            self.velocity.y = self.maxFallSpeed

        if self.wishDir.x != 0:
            target = self.wishDir.x * self.maxAirSpeed
            self.accel_towards(target, self.airAccel, dt)
        else:
            self.apply_friction(self.airFriction, dt)

    # JUMPS
    def try_jump(self):
        if self.jumpBufferTimer > 0:
            self.perform_jump()
            self.jumpBufferTimer = 0

    def perform_jump(self):
        if self.jumpCount < self.maxJump:
            self.velocity.y = -self.jumpPower
            self.jumpCount += 1
            self.coyoteTimer = 0

    # DASH
    def try_dash(self):
        if self.jumpCount <= 1:
            direction = 1 if self.player.facing_right else -1

            if self.wishDir.x == 0:
                direction *= -1

            self.velocity.x = self.dashXStrength * direction
            if not self.player.onGround:
                self.velocity.y = -self.dashYStrength

            self.state = "dashing"
            self.dashTimer = self.dashCooldown
            self.canDash = False

    # SLIDE
    def start_slide(self):
        if not self.sliding and abs(self.velocity.x) > 5:
            self.sliding = True
            self.velocity.x *= 1.10

    def update_slide(self, dt):
        if not self.sliding: 
            return

        self.state = "sliding"
        
        # slow down
        self.apply_friction(self.slideDecay, dt)

        # auto-stop
        if abs(self.velocity.x) < 0.5:
            self.sliding = False

    # MAIN 
    def update(self, dt):

        # TIMERS
        if self.jumpBufferTimer > 0:
            self.jumpBufferTimer -= dt
        if self.coyoteTimer > 0:
            self.coyoteTimer -= dt
        if self.jumpCDTimer > 0:
            self.jumpCDTimer -= dt
        if not self.canDash:
            self.dashTimer -= dt
            if self.dashTimer <= 0:
                self.canDash = True


        # INPUT
        self.update_wishdir()

        if self.wishDir.x > 0:
            self.player.facing_right = True
            self.state = "running"
        elif self.wishDir.x < 0:
            self.player.facing_right = False
            self.state = "running"

        if self.player.movement["jump"]:
            self.jumpBufferTimer = self.jumpBufferTime
            self.state = "jumping"

        if self.player.movement["slide"] and self.player.onGround:
            self.start_slide()
        elif not self.player.movement["slide"]:
            self.sliding = False

        if self.player.movement["dash"] and self.canDash and not self.sliding:
            self.try_dash()


        # STATE HANDLING
        if self.sliding:
            self.update_slide(dt)
        else:
            if self.player.onGround:
                self.jumpCount = 0
                self.coyoteTimer = self.coyoteTime
                self.ground_move(dt)
            else:
                if self.player.movement["jump"] and self.sliding and self.player.onGround:
                    self.sliding = False
                    self.perform_jump()
                self.air_move(dt)

        if self.coyoteTimer > 0:
            self.try_jump()

        # ---------------------------------------
        self.player.rect.x += self.velocity.x * dt * 60
        self.player.rect.y += self.velocity.y * dt * 60
