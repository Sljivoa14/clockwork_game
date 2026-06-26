"""
world.py
--------
Tile map: procedural city generation, asset loading, collision, drawing.

Tile IDs:
  0  GRASS
  1  ROAD
  2  SIDEWALK
  3  BUILDING            original brick (outer wall)
  4  TREE                tile_tree.png
  5  TREE2               tile_tree2.png
  6  BUILDING2           tile_building2.png
  7  BUILDING_OFFICE     building_office.png
  8  BUILDING_SHOP       building_shop.png
  9  BUILDING_TENEMENT   building_tenement.png
  10 BUILDING_BRUTALIST  building_brutalist.png
"""

import random
import pygame
from settings import (
    TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT,
    RENDER_WIDTH, RENDER_HEIGHT, BLOCK_SIZE,
)

# ── Tile ID constants ──────────────────────────────────────────────────────────
GRASS               = 0
ROAD                = 1
SIDEWALK            = 2
BUILDING            = 3
TREE                = 4
TREE2               = 5
BUILDING2           = 6
BUILDING_OFFICE     = 7
BUILDING_SHOP       = 8
BUILDING_TENEMENT   = 9
BUILDING_BRUTALIST  = 10

SOLID_TILES = {
    BUILDING, BUILDING2,
    BUILDING_OFFICE, BUILDING_SHOP,
    BUILDING_TENEMENT, BUILDING_BRUTALIST,
    TREE, TREE2,
}

# Building styles randomly assigned to city blocks
INTERIOR_BUILDINGS = [
    BUILDING, BUILDING2,
    BUILDING_OFFICE, BUILDING_SHOP,
    BUILDING_TENEMENT, BUILDING_BRUTALIST,
]


def _free_bands(blocked: set, length: int):
    """Return (start, end) inclusive index ranges NOT in `blocked`."""
    bands, start = [], None
    for i in range(length):
        if i not in blocked:
            if start is None:
                start = i
        else:
            if start is not None:
                bands.append((start, i - 1))
                start = None
    if start is not None:
        bands.append((start, length - 1))
    return bands


def generate_map():
    """
    1. Outer ring of BUILDING tiles.
    2. Road grid (2-tile roads + 1-tile sidewalks) every BLOCK_SIZE tiles.
    3. Each city block is randomly a building (random style, 1-tile grass
       yard) or a park (grass + scattered TREE/TREE2).
    """
    W, H = WORLD_WIDTH, WORLD_HEIGHT
    grid = [[GRASS] * W for _ in range(H)]

    # Outer wall
    for x in range(W):
        grid[0][x] = BUILDING
        grid[H-1][x] = BUILDING
    for y in range(H):
        grid[y][0] = BUILDING
        grid[y][W-1] = BUILDING

    # Road grid
    road_xs, walk_xs = set(), set()
    for i in range(BLOCK_SIZE, W-1, BLOCK_SIZE):
        for r in (i, i+1):
            if 0 < r < W-1: road_xs.add(r)
        for s in (i-1, i+2):
            if 0 < s < W-1: walk_xs.add(s)

    road_ys, walk_ys = set(), set()
    for i in range(BLOCK_SIZE, H-1, BLOCK_SIZE):
        for r in (i, i+1):
            if 0 < r < H-1: road_ys.add(r)
        for s in (i-1, i+2):
            if 0 < s < H-1: walk_ys.add(s)

    for y in range(1, H-1):
        for x in range(1, W-1):
            if x in road_xs or y in road_ys:
                grid[y][x] = ROAD
            elif x in walk_xs or y in walk_ys:
                grid[y][x] = SIDEWALK

    # City blocks
    x_bands = [(s,e) for s,e in _free_bands(road_xs|walk_xs, W)
               if e > 0 and s < W-1]
    y_bands = [(s,e) for s,e in _free_bands(road_ys|walk_ys, H)
               if e > 0 and s < H-1]

    rng = random.Random(99)  # fixed seed = same map every run

    for (x0, x1) in x_bands:
        for (y0, y1) in y_bands:
            bw = x1 - x0 + 1
            bh = y1 - y0 + 1

            if rng.random() < 0.55 and bw >= 3 and bh >= 3:
                # Building block: random style, 1-tile grass yard around edge
                style = rng.choice(INTERIOR_BUILDINGS)
                for y in range(y0, y1+1):
                    for x in range(x0, x1+1):
                        if x in (x0, x1) or y in (y0, y1):
                            grid[y][x] = GRASS
                        else:
                            grid[y][x] = style
            else:
                # Park block: scatter both tree variants
                for y in range(y0, y1+1):
                    for x in range(x0, x1+1):
                        roll = rng.random()
                        if roll < 0.10:
                            grid[y][x] = TREE
                        elif roll < 0.18:
                            grid[y][x] = TREE2

    return grid


def find_open_tile(map_data, rng):
    """Return (tile_x, tile_y) of a random walkable tile, for spawning."""
    H = len(map_data)
    W = len(map_data[0])
    while True:
        x = rng.randint(1, W-2)
        y = rng.randint(1, H-2)
        if map_data[y][x] not in SOLID_TILES:
            return x, y


class World:
    def __init__(self):
        self.map_data = generate_map()
        self.width    = WORLD_WIDTH
        self.height   = WORLD_HEIGHT
        self._load_tiles()

    def _load_tiles(self):
        def load(path):
            return pygame.image.load(path).convert_alpha()

        raw = {
            GRASS:              load("assets/tile_grass.png"),
            ROAD:               load("assets/tile_road.png"),
            SIDEWALK:           load("assets/tile_sidewalk.png"),
            BUILDING:           load("assets/tile_building.png"),
            BUILDING2:          load("assets/tile_building2.png"),
            BUILDING_OFFICE:    load("assets/building_office.png"),   # NOTE: was comma not dot in your version
            BUILDING_SHOP:      load("assets/building_shop.png"),
            BUILDING_TENEMENT:  load("assets/building_tenement.png"),
            BUILDING_BRUTALIST: load("assets/building_brutalist.png"),
            TREE:               load("assets/tile_tree.png"),
            TREE2:              load("assets/tile_tree2.png"),
        }

        # Composite both tree types onto a grass background
        grass = raw[GRASS]
        for tree_id in (TREE, TREE2):
            composite = grass.copy()
            composite.blit(raw[tree_id], (0, 0))
            raw[tree_id] = composite

        self.tile_images = raw

    def tile_at(self, tile_x, tile_y):
        tile_x = max(0, min(self.width  - 1, tile_x))
        tile_y = max(0, min(self.height - 1, tile_y))
        return self.map_data[tile_y][tile_x]

    def is_solid_pixel(self, px, py):
        return self.tile_at(int(px // TILE_SIZE), int(py // TILE_SIZE)) in SOLID_TILES

    def rect_collides(self, rect):
        corners = [
            (rect.left,    rect.top),
            (rect.right-1, rect.top),
            (rect.left,    rect.bottom-1),
            (rect.right-1, rect.bottom-1),
        ]
        return any(self.is_solid_pixel(cx, cy) for cx, cy in corners)

    def pixel_width(self):  return self.width  * TILE_SIZE
    def pixel_height(self): return self.height * TILE_SIZE

    def draw(self, surface, camera_x, camera_y):
        start_x = int(camera_x // TILE_SIZE)
        start_y = int(camera_y // TILE_SIZE)
        cols = RENDER_WIDTH  // TILE_SIZE + 2
        rows = RENDER_HEIGHT // TILE_SIZE + 2

        for ty in range(start_y, start_y + rows):
            for tx in range(start_x, start_x + cols):
                if 0 <= tx < self.width and 0 <= ty < self.height:
                    img = self.tile_images[self.map_data[ty][tx]]
                    surface.blit(img, (
                        tx * TILE_SIZE - camera_x,
                        ty * TILE_SIZE - camera_y,
                    ))