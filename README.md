# Pixel City - Prototype (v0.4.0)

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
- 1 : equip sword
- 2 : equip gun
- SPACE: sword swing
- F :shoot (gun)
## WILL BE CHANGED TO THE MOUSE CONTROLLS AFTER THE GAME IS FINISHED
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
| `bullet.py`    | the phisics of trajectery of the bullet |
| `npc_0.png`    | npc n1 |
| `npc_1.png`    | npc n2 |
| `npc_2.png`    | npc n3|
| `npc_4.png`    | npc n4 |
| `buidlings`    | diff types of building |
| `building_brutalist.png` | brutalist type of building |
| `building_office.png` | office type of buidling |
|`building_shop.png`| shop look alike building |
|`building_tenement.png`| a tenement style building |
| `tile`         | diff types of tiles ( grass, sidewalk, road, trees, and more soon..) |

## What's next !
YOU MAY READ THE NEXT AddOns in the Future.plan file!
<pre>
   
# GAME DEVELOPMENT .PLAN

## Project

Game: [CLOCKWORK_ORANGE]

Current Version: v0.4.0

Status: In Development

---

# CURRENT FOCUS

* [ WEAPONS_USAGE ] [done]
* [ NPC_BEHAVIOR ] [done]
    |-> 1.COP, 2. normal npc's
* [ BUGS_IN_GENERAL_ ] [side]

---

# FUTURE ADD-ONS

X = done
empty = not done
## Gameplay
-> fo the charecter
* [ JOBS ] X
* [ ILLIGAL_JOBS] X
* [ MONEY ] X
* [ AI_implemantation] 

## Content

* [ no plan 4 that yet ] [New levels]
* [ making the map bigger ] [New maps]
* [ 3-6 ] [New enemies]
* [ freinds ] [New characters]
* [ bags, in-game drugs, ] [New items]
* [ None ] [New missions]

## Progression

* [ X ] [XP system]
* [ ] [Leveling system]
* [ ] [Unlockable content]
* [ ] [Achievements]
* [ ] [Ranks or leaderboards]

## UI / UX
* [ ] [Better HUD]
* [ ] [Animations]
* [ ] [Sound effects]
* [ ] [Music]

## Technical

* [ ] [Save system]
* [ ] [Loading system]
* [ ] [Performance optimization]
* [ ] [Mobile support]
* [ ] [Controller support]
* [ ] [Online/multiplayer functionality]

---

# BUGS

## CRITICAL

Bugs that break the game or make it impossible to continue.

* [ MOVEMENT ] [done]
* [ WEAPONS_USAGE] [done]

## HIGH PRIORITY

Major bugs that significantly affect gameplay.

* [ NPC_BEHAVIOR ] [done]
* [ NPC_DAMAGE] [done]

## LOW PRIORITY

Minor bugs that do not seriously affect gameplay.

* [ ] [Bug description]
* [ ] [Bug description]

---


---

# IMPROVEMENTS

Things that already work but could become better.
Y = yes
N = no

* [ Y ] Improve [system]
* [ Y ] Make [feature] faster
* [ Y ] Improve animations
* [ Y ] Improve graphics
* [ Y ] Improve sound design
* [ Y ] Improve controls
* [ Y ] Improve performance
* [ Y ] Improve code organization

---

# IDEAS

Random ideas that may or may not become actual features.

* [ More realistic ] [Idea]


---

# CURRENT PROBLEMS

Problems that need investigation.

* [ ] [Problem]
* [ ] [Problem]

---

# NEXT MILESTONE

## Version 0.6.0

### Main Goal
MAKE THE GAME PLAYEBLE BY AN AI and OBSERVE WHAT HAPPENS!!!

</pre>

This is intentionally minimal so the code stays readable: 
<p size= "300px">SPLEASE NOTE THAT IF YOU ARE READING THIS THAT THE GAME IS STILL PROGRESS!!!</p>

## Notes on the art style

All art is procedurally generated in `assets_gen.py` using Pillow -
literally setting individual pixel colors. Open that file and tweak
colors/shapes to give your character and city their own look. This
also means the project has zero dependency on any external images.
