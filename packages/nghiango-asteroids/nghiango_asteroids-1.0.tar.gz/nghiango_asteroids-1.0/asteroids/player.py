import pygame

from asteroids.circleshape import CircleShape
from asteroids.constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_SHOOT_COOLDOWN,
)
from asteroids.shot import Shot


# Class for game player objects
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cd = 0

    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, "white", points, width=2)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_cd -= dt
        if self.shoot_cd < 0:
            self.shoot_cd = 0

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_j] or keys[pygame.K_SPACE]:
            self.shoot(dt)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        distance = PLAYER_SPEED * dt
        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)

        self.position += forward_vector * distance

    def shoot(self, dt):
        if self.shoot_cd > 0:
            return
        self.shoot_cd = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)

        shot.velocity = forward_vector * PLAYER_SHOOT_SPEED
