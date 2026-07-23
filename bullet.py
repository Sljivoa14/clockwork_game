"""
bullet.py
---------
A single bullet fired by the player.
Travels in a straight line until it hits an NPC or travels too far.
"""

import pygame
from settings import BULLET_SPEED, BULLET_MAX_RANGE

DIR_VECTORS = {
    "up" : (0, -1),
    "down" : (0, 1),
    "left": (-1, 0),
    "right" : (1, 0)
}

class Bullet:
    def __init__(self, x, y, facing):
        self.x = float(x)
        self.y = float(y)
        self.dx, self.dy = DIR_VECTORS[facing]
        self.distance_travelled = 0.0
        self.alive = True

        # Visual: a tiny 3x3 bright rectangle
        self.size = 1 #or 2

    def update(self, world):
        if not self.alive:
            return
        self.x += self.dx * BULLET_SPEED
        self.y += self.dy * BULLET_SPEED
        self.distance_travelled += BULLET_SPEED

        # Disappear if it hits a wall or travels too far
        if self.distance_travelled >= BULLET_MAX_RANGE:
            self.alive = False
        elif world.is_solid_pixel(self.x, self.y):
            self.alive = False

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    
    def draw(self, surface, camera_x, camera_y):
        if not self.alive:
            return
        pygame.draw.rect(surface, (255, 230, 80),
                         (int(self.x - camera_x), int(self.y - camera_y), self.size, self.size))
