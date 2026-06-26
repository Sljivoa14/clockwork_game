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

## How the code is organized

| File           | What it does |
|----------------|--------------|
| `settings.py`  | All the tunable numbers (window size, speed, tile size...) |
| `assets_gen.py`| Generates the pixel-art PNGs into `assets/` |
| `world.py`     | The tile map: what tiles exist, where, and which are solid |
| `player.py`    | The player: position, input handling, collision, animation |
| `main.py`      | The game loop that ties it all together |
| `npc_0.png`    | npc n1 |
| `npc_1.png`    | npc n2 |
| `npc_2.png`    | npc n3|
| `npc_4.png`    | npc n4 |
| `buidlings`    | diff types of building |
| `tile`         | diff types of tiles |
## What's next (suggested order)

This is intentionally minimal so the code stays readable. Good next
steps, roughly easiest -> hardest:

1. **More map variety** - add more building shapes, alleys, a park,
   maybe a second "district" by expanding `generate_map()`.
2. **NPCs** - other characters that wander around or stand still.
   Reuse the `Player` class as a base for an `NPC` class.
3. **Interactions** - press a key near an NPC/object to trigger a
   dialogue box or action.
4. **A simple stat system** - health, "trouble" meter, etc. shown as
   a small HUD drawn on the render surface.
5. **The AI-driven character idea** - once NPCs and a basic
   action system exist (move, talk, fight, steal...), we can write
   an agent that observes the game state (as a small JSON snapshot)
   and picks actions based on a personality/goal prompt sent to an
   LLM. That becomes a separate `ai_agent.py` module that plugs into
   the existing NPC update loop.
6. **Web version** - once the core mechanics feel good, the same
   ideas (tile grid, sprite, camera) translate directly to a
   JS/Canvas version if you want it playable in-browser.

## Notes on the art style

All art is procedurally generated in `assets_gen.py` using Pillow -
literally setting individual pixel colors. Open that file and tweak
colors/shapes to give your character and city their own look. This
also means the project has zero dependency on any external images.
