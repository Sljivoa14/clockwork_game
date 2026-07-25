"""
main.py
_______

The entry point. This is where the actual "game loop" lives:

    while running:
        1. handle input/events
        2. update game state
        3. draw everything

Run with:
    python main.py
        Game loop: input → update → draw
Controls:
    WASD / arrows  move
    1              equip sword
    2              equip gun
    SPACE          sword swing
    F              shoot (gun)
    ESC            quit
"""
import random
import pygame

from settings import (
    RENDER_WIDTH, RENDER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    FPS, BLACK, TILE_SIZE, NPC_COUNT,
    PLAYER_MAX_HP, WANTED_MAX, WANTED_DECAY_TIME,
    NPC_CONTACT_DAMAGE, BULLET_DAMAGE,
    MONEY_SPAWN_CHANCE_PER_SECOND, MONEY_PICKUP_SIZE, MONEY_VALUE,
    MONEY_COLOR, XP_BAR_WIDTH, XP_BAR_HEIGHT, XP_BAR_COLOR,
    XP_PER_KILL, XP_PER_PICKUP, XP_TO_LEVEL,
    COP_SPEED, COP_SPAWN_ON_CRIME, COP_CHASE_RANGE,
)

from world import World, find_open_tile, ROAD, SIDEWALK

from player import Player
from npc import NPC
from cop import Cop

CIVILIAN_SPRITES = [
    "assets/npc_0.png",
    "assets/npc_1.png",
    "assets/npc_2.png",
    "assets/npc_4.png",
]
COP_SPRITE = "assets/cop.png"

# Wanted star colors for the HUD
STAR_FULL  = (255, 210,  0)
STAR_EMPTY = ( 60,  60, 60)

def compute_camera(player, World):
    cam_x = player.x + TILE_SIZE / 2 - RENDER_WIDTH  / 2
    cam_y = player.y + TILE_SIZE / 2 - RENDER_HEIGHT / 2
    cam_x = max(0, min(cam_x, World.pixel_width()  - RENDER_WIDTH))
    cam_y = max(0, min(cam_y, World.pixel_height() - RENDER_HEIGHT))
    return cam_x, cam_y


def spawn_npcs(world, rng):
    npcs = []
    for _ in range(NPC_COUNT):
        tx, ty = find_open_tile(world.map_data, rng)
        sprite  = rng.choice(CIVILIAN_SPRITES)
        npcs.append(NPC(tx * TILE_SIZE, ty * TILE_SIZE, sprite, rng))
    return npcs

def spawn_cop(world, rng):
    tx, ty = find_open_tile(world.map_data, rng)
    return Cop(tx * TILE_SIZE, ty * TILE_SIZE, COP_SPRITE, rng)

def spawn_money_random(world, rng): # we have a 1% chance to find money randomly on the floor
    while True:
        tx, ty  = find_open_tile(world.map_data, rng)
        tile = world.tile_at(tx, ty)
        if tile in (ROAD, SIDEWALK):
            break
    return {
        "x": tx * TILE_SIZE + TILE_SIZE // 2,
        "y": ty * TILE_SIZE + TILE_SIZE // 2,
        "value": MONEY_VALUE
    }


def draw_hud(surface, player, wanted_level):
    """
    Draw the HUD directly onto the small render_surface (before scaling),
    so it stays crisp at native resolution.

    Layout (top-left corner):
      ♥ health bar (green → red as HP drops)
      ★ wanted stars (1-5)
      weapon indicator text
    """
    pad = 3

    # ── Health bar ───────────────────────────────────────────────────────────
    bar_w  = 60
    bar_h  = 6
    bar_x  = pad
    bar_y  = pad

    # Background (dark red)
    pygame.draw.rect(surface, (120, 20, 20), (bar_x, bar_y, bar_w, bar_h))

    # Foreground (bright green → orange → red based on HP %)
    hp_pct  = player.hp / player.max_hp
    fill_w  = int(bar_w * hp_pct)
    if hp_pct > 0.5:
        bar_color = (50, 200, 50)
    elif hp_pct > 0.25:
        bar_color = (220, 160, 0)
    else:
        bar_color = (220, 40, 40)

    if fill_w > 0:
        pygame.draw.rect(surface, bar_color, (bar_x, bar_y, fill_w, bar_h))
    # Thin white border
    pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 1)

    # ── Wanted stars ─────────────────────────────────────────────────────────
    star_y   = bar_y + bar_h + 3
    star_size = 5
    star_gap  = 2
    for i in range(WANTED_MAX):
        color = STAR_FULL if i < wanted_level else STAR_EMPTY
        sx = pad + i * (star_size + star_gap)
        pygame.draw.rect(surface, color, (sx, star_y, star_size, star_size))

    weapon_color = (255, 255, 100) if player.weapon == "gun" else (200, 200, 200)
    wx = pad
    wy = star_y + star_size + 3
    pygame.draw.rect(surface, weapon_color, (wx, wy, 5, 5))

    # Top-right money + xp
    font = pygame.font.Font(None, 16)
    money_text = font.render(f"${player.money}", True, MONEY_COLOR)
    mx = RENDER_WIDTH - money_text.get_width() - pad
    my = pad
    surface.blit(money_text, (mx, my))

    xp_x = RENDER_WIDTH - XP_BAR_WIDTH - pad
    xp_y = my + money_text.get_height() + 4
    xp_pct = min(1.0, player.xp / player.xp_to_next_level)
    pygame.draw.rect(surface, (40, 40, 40), (xp_x, xp_y, XP_BAR_WIDTH, XP_BAR_HEIGHT))
    pygame.draw.rect(surface, XP_BAR_COLOR, (xp_x, xp_y, int(XP_BAR_WIDTH * xp_pct), XP_BAR_HEIGHT))
    pygame.draw.rect(surface, (200, 200, 200), (xp_x, xp_y, XP_BAR_WIDTH, XP_BAR_HEIGHT), 1)


def main():
    pygame.init()
    pygame.display.set_caption("Pixel City")

    window         = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    render_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))
    clock          = pygame.time.Clock()

    world = World()
    rng   = random.Random(123)

    tx, ty = find_open_tile(world.map_data, random.Random(1))
    player = Player(tx * TILE_SIZE, ty * TILE_SIZE)
    player.money =  50
    player.xp = 0
    player.xp_to_next_level = XP_TO_LEVEL   
    npcs   = spawn_npcs(world, rng)
    money_pickups = []

    def spawn_cops_4_crime():
        for _ in range(COP_SPAWN_ON_CRIME):
            npcs.append(spawn_cop(world, rng))
    # Wanted system state
    wanted_level       = 0          # 0-5 stars
    wanted_decay_timer = 0.0        # counts up; resets when player hits someone

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    player.try_attack()
                elif event.key == pygame.K_f:
                    player.try_shoot()

        # ── Update ────────────────────────────────────────────────────────────
        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt, world)

        player_rect = player.get_rect()

        # Sword hits
        if player.is_attacking:
            attack_rect = player.get_attack_rect()
            for npc in npcs:
                if npc.alive and npc.flee_timer <= 0:
                    if attack_rect.colliderect(npc.get_rect()):
                        npc.take_hit(34)
                        # Each sword hit adds to the chaos meter
                        wanted_level       = min(WANTED_MAX, wanted_level + 1)
                        wanted_decay_timer = 0.0   # reset decay clock
                        # Reward XP and alert cops
                        player.earn_xp(XP_PER_KILL)
                        spawn_cops_4_crime()

        # Bullet hits
        for bullet in player.bullets:
            if not bullet.alive:
                continue
            for npc in npcs:
                if npc.alive and bullet.get_rect().colliderect(npc.get_rect()):
                    npc.take_hit(BULLET_DAMAGE)
                    bullet.alive = False
                    wanted_level       = min(WANTED_MAX, wanted_level + 1)
                    wanted_decay_timer = 0.0
                    # Reward XP and alert cops
                    player.earn_xp(XP_PER_KILL)
                    spawn_cops_4_crime()
                    break

        # Update NPCs; collect any contact damage they want to deal
        for npc in npcs:
            npc.update(dt, world, player_rect, wanted_level)
            if npc._wants_to_damage_player:
                player.take_damage(NPC_CONTACT_DAMAGE)

        # Remove dead NPCs
        npcs = [n for n in npcs if n.alive]

        # Money spawn (random on roads/sidewalks) and pickup handling
        if rng.random() < MONEY_SPAWN_CHANCE_PER_SECOND * dt:
            money_pickups.append(spawn_money_random(world, rng))

        new_money_pickups = []
        for pickup in money_pickups:
            pickup_rect = pygame.Rect(
                int(pickup["x"] - MONEY_PICKUP_SIZE / 2),
                int(pickup["y"] - MONEY_PICKUP_SIZE / 2),
                MONEY_PICKUP_SIZE, MONEY_PICKUP_SIZE
            )
            if player_rect.colliderect(pickup_rect):
                player.earn_money(pickup["value"])
                player.earn_xp(XP_PER_PICKUP)
            else:
                new_money_pickups.append(pickup)
        money_pickups = new_money_pickups

        # Wanted decay: reduce one star if player lays low long enough
        if wanted_level > 0:
            wanted_decay_timer += dt
            if wanted_decay_timer >= WANTED_DECAY_TIME:
                wanted_level       = max(0, wanted_level - 1)
                wanted_decay_timer = 0.0

        # Check player death
        if not player.alive:
            running = False  # for now — later we can show a death screen

        cam_x, cam_y = compute_camera(player, world)

        # ── Draw ──────────────────────────────────────────────────────────────
        render_surface.fill(BLACK)
        world.draw(render_surface, cam_x, cam_y)

        # Draw money pickups
        for pickup in money_pickups:
            px = int(pickup["x"] - cam_x)
            py = int(pickup["y"] - cam_y)
            pygame.draw.rect(render_surface, MONEY_COLOR,
                             (px - MONEY_PICKUP_SIZE//2, py - MONEY_PICKUP_SIZE//2,
                              MONEY_PICKUP_SIZE, MONEY_PICKUP_SIZE))

        for npc in npcs:
            npc.draw(render_surface, cam_x, cam_y)
        player.draw(render_surface, cam_x, cam_y)

        draw_hud(render_surface, player, wanted_level)

        scaled = pygame.transform.scale(render_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()