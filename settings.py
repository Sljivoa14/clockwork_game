"""
settings.py
-----------
All the "tunable knobs" for the game live here. Keeping constants in one
place means if you want to make the player faster, or the window bigger,
you change ONE number instead of hunting through every file.

5
"""

# --- Pixel art resolution ---
TILE_SIZE = 16          # every tile and the player sprite are 16x16 pixels
SCALE = 3                # we draw everything tiny, then blow it up by this
                         # factor so it looks like a chunky retro game

# --- "Camera" / internal resolution ---
# This is the size of the surface we actually draw the game onto.
# Think of it as the resolution of an old console.
VIEW_TILES_X = 20
VIEW_TILES_Y = 15
RENDER_WIDTH = VIEW_TILES_X * TILE_SIZE    # 320
RENDER_HEIGHT = VIEW_TILES_Y * TILE_SIZE   # 240

# --- Real window size shown on your screen ---
WINDOW_WIDTH = RENDER_WIDTH * SCALE        # 960
WINDOW_HEIGHT = RENDER_HEIGHT * SCALE      # 720

# --- World size (in tiles) ---
WORLD_WIDTH = 130
WORLD_HEIGHT = 100
BLOCK_SIZE = 12

# --- Misc ---
FPS = 60
PLAYER_SPEED = 1.5   # pixels per frame, at native (16px) resolution

#---NPC----
NPC_COUNT = 30
NPC_SPEED = 0.9
NPC_FLEE_SPEED = 2

#---COMBAT---
ATTACK_DURATION= 0.3
ATTACK_REACH_MELEE = 5
ATTACK_REACH_GUN = 30
ATTACK_COOLDOWN = 0.25


# --- Colors (used for things we don't load as images, e.g. background) ---
BLACK = (0, 0, 0)
RED_FLASH = (220, 60, 60)

#Player health
PLAYER_MAX_HP   = 100
NPC_CONTACT_DAMAGE = 8

#WANTED 
WANTED_MAX = 5
WANTED_DECAY_TIME = 8.2

#GUN
BULLET_SPEED = 2
BULLET_DAMAGE= 40
BULLET_MAX_RANGE = 220
