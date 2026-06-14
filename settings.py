"""
settings.py
-----------
All the "tunable knobs" for the game live here. Keeping constants in one
place means if you want to make the player faster, or the window bigger,
you change ONE number instead of hunting through every file.
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
WORLD_WIDTH = 40
WORLD_HEIGHT = 30

# --- Misc ---
FPS = 60
PLAYER_SPEED = 1.5   # pixels per frame, at native (16px) resolution

# --- Colors (used for things we don't load as images, e.g. background) ---
BLACK = (0, 0, 0)
