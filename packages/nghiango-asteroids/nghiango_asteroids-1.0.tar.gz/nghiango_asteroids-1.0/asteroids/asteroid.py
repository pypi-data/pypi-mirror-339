import random

import pygame

from asteroids.circleshape import CircleShape
from asteroids.constants import ASTEROID_MIN_RADIUS


# Class for game asteroid objects
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2)

    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        self.position += self.velocity * dt

    def split(self):
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20, 50)

        left_split_velocity = self.velocity.rotate(angle)
        right_split_velocity = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        left_split = Asteroid(self.position.x, self.position.y, new_radius)
        left_split.velocity = left_split_velocity * 1.2

        right_split = Asteroid(self.position.x, self.position.y, new_radius)
        right_split.velocity = right_split_velocity * 1.2
