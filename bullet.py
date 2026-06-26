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
    "left ": (-1, 0),
    "right" : (1, 0)
}

class bullet:
    def __init__(self, x, y, facing):
        self.x = float (x)
        self.y = float(y)
        self.dx, self.dy = DIR_VECTORS[facing]
        self.distance_travelled = 0.0
        self.alive = True

        self.size = 3
        
