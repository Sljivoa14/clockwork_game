"""
world.py
--------
Defines the game world: a grid of tiles, which tiles you can walk on
vs. which block you, and how to draw the visible part of the map.

The map is represented as a 2D list of integers. Each integer is a
"tile ID" that maps to a tile type (grass, road, building, etc.).
This is a very common way games store maps - you'll see the same idea
in tools like Tiled (a popular free map editor).
"""

import random
import pygame
from settings import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, RENDER_WIDTH, RENDER_HEIGHT

# --- Tile IDs ---
GRASS = 0
ROAD = 1
SIDEWALK = 2
BUILDING = 3
TREE = 4

# Which tile IDs the player CANNOT walk through.
SOLID_TILES = {BUILDING, TREE}


def generate_map():
    """
    Builds the starting area as a 2D list: map_data[y][x] -> tile id.

    Layout idea:
    - A ring of buildings around the whole map (so the player can't
      wander off into the void yet).
    - A horizontal road + vertical road crossing in the middle, each
      with sidewalks on either side.
    - The rest is grass, with a handful of trees scattered around.
    """
    width, height = WORLD_WIDTH, WORLD_HEIGHT
    map_data = [[GRASS for _ in range(width)] for _ in range(height)]

    # --- Outer wall of buildings ---
    for x in range(width):
        map_data[0][x] = BUILDING
        map_data[height - 1][x] = BUILDING
    for y in range(height):
        map_data[y][0] = BUILDING
        map_data[y][width - 1] = BUILDING

    # --- Horizontal road across the middle, with sidewalks ---
    road_row = height // 2
    for x in range(width):
        map_data[road_row - 1][x] = SIDEWALK
        map_data[road_row][x] = ROAD
        map_data[road_row + 1][x] = ROAD
        map_data[road_row + 2][x] = SIDEWALK

    # --- Vertical road down the middle, with sidewalks ---
    road_col = width // 2
    for y in range(height):
        map_data[y][road_col - 1] = SIDEWALK
        map_data[y][road_col] = ROAD
        map_data[y][road_col + 1] = ROAD
        map_data[y][road_col + 2] = SIDEWALK

    # --- Scatter some trees on the grass (deterministic so the map
    #     is the same every time you run the game) ---
    rng = random.Random(42)
    for _ in range(30):
        x = rng.randint(2, width - 3)
        y = rng.randint(2, height - 3)
        if map_data[y][x] == GRASS:
            map_data[y][x] = TREE

    return map_data


class World:
    def __init__(self):
        self.map_data = generate_map()
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT

        # Load each tile image once and keep them in a dict for quick lookup.
        self.tile_images = {
            GRASS: pygame.image.load("assets/tile_grass.png").convert_alpha(),
            ROAD: pygame.image.load("assets/tile_road.png").convert_alpha(),
            SIDEWALK: pygame.image.load("assets/tile_sidewalk.png").convert_alpha(),
            BUILDING: pygame.image.load("assets/tile_building.png").convert_alpha(),
            BUILDING2: pygame.image.load("assets/tile_building2.png").convert_alpha(),
            BUILDING3: pygame.image.load("").convert_alpha(),
            BUILDING4: pygame.image.load("").convert_alpha(),
            BUILDING5: pygame.image.load("").convert_alpha(),
            TREE: pygame.image.load("assets/tile_tree.png").convert_alpha(),
        }
        # Trees are drawn on top of grass, so pre-render a grass+tree tile.
        grass_and_tree = self.tile_images[GRASS].copy()
        grass_and_tree.blit(self.tile_images[TREE], (0, 0))
        self.tile_images[TREE] = grass_and_tree

    def tile_at(self, tile_x, tile_y):
        """Return the tile ID at a given tile coordinate (clamped to map edges)."""
        tile_x = max(0, min(self.width - 1, tile_x))
        tile_y = max(0, min(self.height - 1, tile_y))
        return self.map_data[tile_y][tile_x]

    def is_solid_pixel(self, pixel_x, pixel_y):
        """Is the tile under this world-pixel-coordinate solid (blocks movement)?"""
        tile_x = int(pixel_x // TILE_SIZE)
        tile_y = int(pixel_y // TILE_SIZE)
        return self.tile_at(tile_x, tile_y) in SOLID_TILES

    def pixel_width(self):
        return self.width * TILE_SIZE

    def pixel_height(self):
        return self.height * TILE_SIZE

    def draw(self, surface, camera_x, camera_y):
        """
        Draw only the tiles visible in the camera's view.

        camera_x / camera_y = world pixel coordinates of the top-left
        corner of the screen.
        """
        # Which tile is at the top-left of the screen?
        start_tile_x = int(camera_x // TILE_SIZE)
        start_tile_y = int(camera_y // TILE_SIZE)

        # How many tiles fit on screen? (+2 so we cover partial tiles
        # at the edges when the camera is between tile boundaries)
        tiles_across = RENDER_WIDTH // TILE_SIZE + 2
        tiles_down = RENDER_HEIGHT // TILE_SIZE + 2

        for ty in range(start_tile_y, start_tile_y + tiles_down):
            for tx in range(start_tile_x, start_tile_x + tiles_across):
                if 0 <= tx < self.width and 0 <= ty < self.height:
                    tile_id = self.map_data[ty][tx]
                    image = self.tile_images[tile_id]
                    # Convert this tile's world position to screen position
                    screen_x = tx * TILE_SIZE - camera_x
                    screen_y = ty * TILE_SIZE - camera_y
                    surface.blit(image, (screen_x, screen_y))
