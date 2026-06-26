# Pixel City - Prototype (v0.1)

A tiny top-down open-world prototype built with Python + Pygame.
This is the foundation: a movable character, a tile-based map, a
scrolling camera, and self-generated pixel art (no external assets,
no copyright issues).

## How to run it

1. Make sure you have Python 3.10+ installed.
2. Install the one dependency:
   ```
   pip install -r requirements.txt
   ```
3. Generate the pixel art (only needs to be done once, or whenever
   you tweak `assets_gen.py`):
   ```
   python assets_gen.py
   ```
4. Run the game:
   ```
   python main.py
   ```

## Controls

- Arrow keys or WASD: move around
- ESC: quit
- LEFT-CLICK: shoot
- RIGHT-CLICK: stab

## How the code is organized

| File           | What it does |
|----------------|--------------|
| `settings.py`  | All the tunable numbers (window size, speed, tile size...) |
| `assets_gen.py`| Generates the pixel-art PNGs into `assets/` |
| `world.py`     | The tile map: what tiles exist, where, and which are solid |
| `player.py`    | The player: position, input handling, collision, animation |
| `main.py`      | The game loop that ties it all together |
| `npc.py`       | The behavior of npcs |
| `bullet.py`      | the phisics of trajectery of the bullet |
| `npc_0.png`    | npc n1 |
| `npc_1.png`    | npc n2 |
| `npc_2.png`    | npc n3|
| `npc_4.png`    | npc n4 |
| `buidlings`    | diff types of building |
| `tile`         | diff types of tiles |
## What's next (suggested order)

This is intentionally minimal so the code stays readable: 
<p size= "300px">SPLEASE NOTE THAT IF YOU ARE READING THIS THAT THE GAME IS STILL PROGRESS!!!</p>

## Notes on the art style

All art is procedurally generated in `assets_gen.py` using Pillow -
literally setting individual pixel colors. Open that file and tweak
colors/shapes to give your character and city their own look. This
also means the project has zero dependency on any external images.
