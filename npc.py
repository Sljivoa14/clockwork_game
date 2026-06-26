"""
npc.py
------
NPC: wander, flee when hit, chase + attack when wanted level is high enough.
"""

import pygame
from settings import TILE_SIZE, NPC_SPEED, NPC_FLEE_SPEED, RED_FLASH, NPC_CONTACT_DAMAGE

DIRECTIONS = [(0,0),(1,0),(-1,0),(0,1),(0,-1)]

NPC_MAX_HP        = 60
CHASE_WANTED      = 2      # wanted stars needed before NPCs chase you
CHASE_RANGE       = 80     # pixels — how close before an aggressive NPC chases
CONTACT_DAMAGE_CD = 0.5    # seconds between contact-damage ticks
