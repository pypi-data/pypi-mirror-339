import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we using this already, make me wonder why "containers" even work
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def is_collision(self, other):
        if not isinstance(other, CircleShape):
            print(f"Doesn't supported, got {type(other)} instead of a CircleShape")
            return False
        return self.position.distance_to(other.position) < self.radius + other.radius
