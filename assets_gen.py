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


"""
    16x32 sprite sheet: frame 0 (top 16px) = right leg forward,
    frame 1 (bottom 16px) = left leg forward.
    Both frames have eyes and a mouth now.
"""
def make_person_sheet(jacket=(45,45,50), hair=(40,20,20),
                      pants=(35,35,60),  skin=(224,172,133)):
    sheet = Image.new("RGBA", (TILE, TILE * 2), (0, 0, 0, 0))
    boots = (20, 20, 20)
    eye_color = (30, 20,20)
    mouth_col = (160, 90, 80)
    def draw_base(img):
        #head
        for x in range(5, 11):
            for y in range(1, 6):
                img.putpixel((x, y), skin)
        #hair
        for (x ,y) in [(5,1),(6,0),(7,0),(8,0),(9,0),(10,1),(4,2),(11,2)]:
            img.putpixel((x, y), hair)
        
        #eyes
        img.putpixel((6, 3), eye_color)
        img.putpixel((9,3), eye_color)

        #mouth
        img.putpixel((7, 4), mouth_col)
        img.putpixel((8, 5), mouth_col)

        #torso
        for x in range(4, 12):
            for y in range(6, 12):
                img.putpixel((x, y), jacket)
        for y in range(6, 11):
            img.putpixel((3, y), jacket)
            img.putpixel((12,y), jacket)

    
    #----------Frame 0: right leg forward, left leg back----------
    frame0 = new_tile()
    draw_base(frame0)
    #left leg (back) - shorter, starts lower the the other
    for x in range(6, 8):
        for y in range(13, 16):
            frame0.putpixel((x, y), pants)
        frame0.putpixel((x, 15), boots)
    #right leg (forward) - full lenth
    for x in range(9, 11):
        for y in range(11, 16):
            frame0.putpixel((x, y), pants)
        frame0.putpixel((x, 15), boots)


    #------frame 1: left leg forward, right leg back---------------
    frame1 = new_tile()
    draw_base(frame1)
    #left leg forward /full length
    for x in range(6, 8):
        for y in range(11, 16):
            frame1.putpixel((x, y), pants)
        frame1.putpixel((x, 15), boots)
    #right leg (back) - shorter, starts lower then the other
    for x in range(9, 11):
        for y in range(13, 16):
            frame1.putpixel((x, y), pants)
        frame1.putpixel((x, 15), boots)

    
    sheet.paste(frame0, (0, 0))
    sheet.paste(frame1, (0, TILE))
    return sheet

def make_cop_sheet():
    """
    Police officer: dark blue uniform, gold badge, police cap with brim,
    face with eyes and a stern mouth.

    """
    sheet      = Image.new("RGBA", (TILE, TILE*2), (0,0,0,0))
    uniform    = (40,  60, 120)
    uni_dark   = (28,  42,  88)
    skin       = (224,172, 133)
    badge      = (220,190,  50)
    belt       = (25,  20,  18)
    boots      = (15,  15,  15)
    cap        = (25,  40,  90)
    brim       = (18,  28,  65)
    eye_color  = (25,  15,  15)
    mouth_col  = (130, 70,  65)

#ACAB
    def draw_cop_base(img):
        #cap
        for x in range(4, 12):
            for y in range(0, 2):
                img.output((x, y), cap)

        #Brim
        for x in range(3, 13):
            img.putpixel((x, 2), brim)

        #face 
        for x in range(5, 11):
            for y in range(2, 6):
                img.putpixel((x, y), skin)
        
        #eyes
        img.putpixel((6, 3), eye_color)
        img.putpixel((9, 3), eye_color)
        # Stern straight mouth
        img.putpixel((7, 5), mouth_col)
        img.putpixel((8, 5), mouth_col)

        #uniroform torso
        for x in range(4, 12):
            for y in range(6, 12):
                img.putpixel((x, y), uniform)
        
        #arms
        for y in range(6, 11):
            img.putpixel((3,  y), uniform)
            img.putpixel((12, y), uniform)

        # Gold badge (two pixels on chest)
        img.putpixel((7, 7), badge)
        img.putpixel((8, 7), badge)

        # Belt
        for x in range(4, 12):
            img.putpixel((x, 11), belt)

    #frame 0: right leg forward
    frame0 = new_tile()
    draw_cop_base(frame0)
    for x in range(6, 8):
        for y in range(13, 16):
            frame0.putpixel((x, y), uni_dark)
        frame0.putpixel((x, 15), boots)
    
    for x in range(9, 11):
        for y in range(11, 16):
            frame0.putpixel((x, y), uni_dark)
        frame0.putpixel((x, 15), boots)

    # Frame 1: left leg forward
    frame1 = new_tile()
    draw_cop_base(frame1)
    for x in range(6, 8):
        for y in range(11, 16):
            frame1.putpixel((x, y), uni_dark)
        frame1.putpixel((x, 15), boots)
    for x in range(9, 11):
        for y in range(13, 16):
            frame1.putpixel((x, y), uni_dark)
        frame1.putpixel((x, 15), boots)

    sheet.paste(frame0, (0,    0))
    sheet.paste(frame1, (0, TILE))
    return sheet


def make_sword():
    img = new_tile()
    blade = (200, 200, 210)
    blade_edge = (235, 235, 245)
    guard      = (120,  90,  40)
    handle     = ( 90,  60,  35)

    for y in range(1, 10):
        img.putpixel((7, y), blade)
        img.putpixel((8, y), blade_edge)
    img.putpixel((7, 0), blade_edge)
    img.putpixel((8, 0), blade_edge)
    for x in range(5, 11):
        img.putpixel((x, 10), guard)
    for y in range (11, 15):
        img.putpixel((7, y), handle)
        img.putpixel((8, y), handle)
    
    return img

def make_gun():
    img  = new_tile()
    metal = (80, 82, 88)
    metal_dark = (55,  57,  62)
    metal_light = (120,122, 130)
    grip = (70,  48,  30)
    grip_dark = (50,  32,  18)
    trigger = (90, 90, 95)
    barrel_tip = (50, 50, 55)

    #barrel
    for x in range(4, 14):
        img.putpixel((x, 5), metal_light)
        img.putpixel((x, 6), metal)
        img.putpixel((x, 7), metal_dark)

    #muzzle
    for y in range(5, 8):
        img.putpixel((14, y), barrel_tip)
        img.putpixel((15, y), barrel_tip)
    
    #slide
    for x in range(5, 13):
        img.putpixel((x, 4), metal)
        img.putpixel((x, 8), metal_dark)

    # Body
    for x in range(5, 10):
        for y in range(5, 10):
            img.putpixel((x, y), metal)
        img.putpixel((8, 4), metal_light)
        img.putpixel((9, 4), metal_light)
    
    #trigger guard>
    for (x,y) in [(6,9),(7,9),(8,9),(5,10),(9,10),(5,11),(9,11),(6,12),(7,12),(8,12)]:
        img.putpixel((x, y), metal_dark)
    img.putpixel((7, 10), trigger)
    img.putpixel((7, 11), trigger)

    #grip
    for x in range(4, 9):
        for y in range(9, 15):
            c = grip_dark if (x+y) % 3 == 0 else grip # no ===
            img.putpixel((x, y), c) # cz c == 0 else grip_dark
    for x in range(4, 9):
        img.putpixel((x, 15), grip_dark)
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    assets = {
        "tile_grass.png":          make_grass(),
        "tile_road.png":           make_road(),
        "tile_sidewalk.png":       make_sidewalk(),
        "tile_building.png":       make_building(),
        "tile_tree.png":           make_tree(),
        "player.png":              make_person_sheet(),
        "sword.png":               make_sword(),
        "gun.png":                 make_gun(),
        # NPC colour variants — all now have faces
        "npc_0.png": make_person_sheet(jacket=(150,60,60),  hair=(20,20,20)),
        "npc_1.png": make_person_sheet(jacket=(70,110,150), hair=(80,60,40)),
        "npc_2.png": make_person_sheet(jacket=(150,140,60), hair=(60,30,10)),
        "npc_4.png": make_person_sheet(jacket=(80,120,80),  hair=(30,25,20)),
        "cop.png":   make_cop_sheet(),
    }

    for filename, img in assets.items():
        path = os.path.join(OUT_DIR, filename)
        img.save(path)
        print(f"Wrote {path}")
            
if __name__ == "__main__":
    main()



"""
def make_player_one():
    new = new
    return new

def make_player_two():
    new = new
    return new """
