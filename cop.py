"""
cop.py file
-
COP NPC behavior. cop appears when we did crimes (hurt npcs, and more will be added).
"""

import pygame
from npc import NPC
from settings import (
    TILE_SIZE,
    COP_SPEED,
    COP_CHASE_RANGE,
    COP_CONTACT_DAMAGE_CD,

)

