"""
assets_gen.py
-------------
Generates all the pixel-art images the game needs, using Pillow (PIL).

Why generate art instead of drawing it by hand in an image editor?
- It's reproducible: anyone can run this script and get the same assets.
- It's a nice intro to the idea that "pixel art" is really just a grid
  of colored squares - which is exactly what a 2D list of colors is.
- Zero copyright concerns since every pixel is drawn by code.

Run this once before running main.py:
    python assets_gen.py

It creates an "assets" folder with:
    tile_grass.png
    tile_road.png
    tile_sidewalk.png
    tile_building.png
    tile_tree.png
    player.png   (a 2-frame walk animation, stacked vertically: 16x32)
"""

from PIL import Image
import os

TILE = 16  # every sprite/tile is 16x16 pixels
OUT_DIR = os.path.join(os.path.dirname(__file__), "assets")


def new_tile():
    """Start with a blank, fully transparent 16x16 image."""
    return Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))


def fill(img, color):
    """Fill the whole image with one color."""
    for x in range(TILE):
        for y in range(TILE):
            img.putpixel((x, y), color)


def make_grass():
    img = new_tile()
    base = (51, 122, 56)       # medium green
    speck = (74, 153, 79)      # lighter green speckle
    fill(img, base)
    # Sprinkle some lighter pixels in a fixed pattern so every grass
    # tile looks slightly textured but still tiles seamlessly-ish.
    speckles = [(2, 2), (5, 9), (9, 4), (12, 12), (3, 13), (13, 6), (7, 7)]
    for (x, y) in speckles:
        img.putpixel((x, y), speck)
    return img


def make_road():
    img = new_tile()
    asphalt = (50, 50, 54)
    crack = (66, 66, 70)
    fill(img, asphalt)
    # A couple of "crack" pixels for texture.
    for (x, y) in [(3, 5), (4, 5), (10, 9), (11, 10), (7, 2)]:
        img.putpixel((x, y), crack)
    return img


def make_sidewalk():
    img = new_tile()
    concrete = (158, 158, 150)
    line = (120, 120, 114)
    fill(img, concrete)
    # Grid lines like concrete slabs.
    for x in range(TILE):
        img.putpixel((x, 0), line)
    for y in range(TILE):
        img.putpixel((0, y), line)
    return img


def make_building():
    img = new_tile()
    brick = (120, 60, 50)
    mortar = (90, 44, 38)
    fill(img, brick)
    # Simple brick pattern: horizontal mortar lines every 4px,
    # with bricks offset every other row for a classic look.
    for y in range(0, TILE, 4):
        for x in range(TILE):
            img.putpixel((x, y), mortar)
    for row in range(TILE // 4):
        offset = 4 if row % 2 == 0 else 0
        for x in range(offset, TILE, 8):
            for y in range(row * 4 + 1, row * 4 + 4):
                if y < TILE:
                    img.putpixel((x % TILE, y), mortar)
    return img


def make_tree():
    img = new_tile()
    trunk = (90, 60, 35)
    leaves = (40, 95, 45)
    leaves_dark = (30, 75, 35)
    fill(img, (0, 0, 0, 0))  # keep background transparent
    # Trunk
    for y in range(11, 16):
        for x in range(7, 9):
            img.putpixel((x, y), trunk)
    # Leafy canopy (a rough circle/blob)
    canopy_pixels = []
    for y in range(2, 12):
        for x in range(2, 14):
            dx, dy = x - 7.5, y - 6.5
            if dx * dx + dy * dy <= 30:
                canopy_pixels.append((x, y))
    for (x, y) in canopy_pixels:
        color = leaves_dark if (x + y) % 5 == 0 else leaves
        img.putpixel((x, y), color)
    return img


def make_player_sheet():
    """
    Returns a 16x32 image: two 16x16 frames stacked vertically.
    Frame 0 (top)    = standing
    Frame 1 (bottom) = mid-step (for a simple walk animation)
    """
    sheet = Image.new("RGBA", (TILE, TILE * 2), (0, 0, 0, 0))

    jacket = (45, 45, 50)     # dark jacket
    skin = (224, 172, 133)    # skin tone
    hair = (40, 20, 20)       # dark red-brown hair
    pants = (35, 35, 60)      # dark denim
    boots = (20, 20, 20)

    def draw_base(img):
        # Head
        for x in range(5, 11):
            for y in range(1, 6):
                img.putpixel((x, y), skin)
        # Hair (top of head + a bit on the sides, spiky)
        for (x, y) in [(5, 1), (6, 0), (7, 0), (8, 0), (9, 0), (10, 1), (4, 2), (11, 2)]:
            img.putpixel((x, y), hair)
        # Torso / jacket
        for x in range(4, 12):
            for y in range(6, 12):
                img.putpixel((x, y), jacket)
        # Arms (slightly darker than jacket for shading)
        for y in range(6, 11):
            img.putpixel((3, y), jacket)
            img.putpixel((12, y), jacket)

    # Frame 0: standing, legs together
    frame0 = new_tile()
    draw_base(frame0)
    for x in range(5, 7):
        for y in range(12, 15):
            frame0.putpixel((x, y), pants)
    for x in range(9, 11):
        for y in range(12, 15):
            frame0.putpixel((x, y), pants)
    for x in range(5, 7):
        frame0.putpixel((x, 15), boots)
    for x in range(9, 11):
        frame0.putpixel((x, 15), boots)

    # Frame 1: walking, legs apart (one forward, one back)
    frame1 = new_tile()
    draw_base(frame1)
    for x in range(4, 6):
        for y in range(12, 15):
            frame1.putpixel((x, y), pants)
    for x in range(10, 12):
        for y in range(12, 15):
            frame1.putpixel((x, y), pants)
    for x in range(4, 6):
        frame1.putpixel((x, 15), boots)
    for x in range(10, 12):
        frame1.putpixel((x, 15), boots)

    sheet.paste(frame0, (0, 0))
    sheet.paste(frame1, (0, TILE))
    return sheet


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    tiles = {
        "tile_grass.png": make_grass(),
        "tile_road.png": make_road(),
        "tile_sidewalk.png": make_sidewalk(),
        "tile_building.png": make_building(),
        "tile_tree.png": make_tree(),
        "player.png": make_player_sheet(),
    }

    for filename, img in tiles.items():
        path = os.path.join(OUT_DIR, filename)
        img.save(path)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
