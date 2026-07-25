"""
npc.py
------
NPC: wander, flee when hit, chase + attack when wanted level is high enough.
"""

import pygame
from settings import TILE_SIZE, NPC_SPEED, NPC_FLEE_SPEED, RED_FLASH, NPC_CONTACT_DAMAGE

DIRECTIONS = [(0,0),(1,0),(-1,0),(0,1),(0,-1)]

NPC_MAX_HP        = 60
CHASE_WANTED      = 2      # wanted stars needed before NPCs chase you
CHASE_RANGE       = 80     # pixels — how close before an aggressive NPC chases
CONTACT_DAMAGE_CD = 0.5    # seconds between contact-damage ticks

class NPC:
    def __init__(self, x, y, sprite_path, rng, role = "civilian"):
        self.x   = float(x)
        self.y   = float(y)
        self.rng = rng
        self.role = role
        self.is_cop = role == "cop"

        sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = {
            "stand": sheet.subsurface(pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)),
            "walk":  sheet.subsurface(pygame.Rect(0, TILE_SIZE, TILE_SIZE, TILE_SIZE)),
        }
        self.facing_left   = False
        self.anim_timer    = 0.0
        self.anim_speed    = 0.18
        self.current_frame = "stand"

        # Health
        self.hp    = NPC_MAX_HP
        self.alive = True

        # Wander state
        self.direction  = (0, 0)
        self.move_timer = 0.0
        self.idle_timer = 0.0
        self.pause_timer = 0.0
        self._pick_direction()

        # Reaction timers
        self.flee_timer       = 0.0
        self.hit_flash_timer  = 0.0
        self.contact_dmg_timer = 0.0   # cooldown so contact damage isn't instant per-frame
        self._wants_to_damage_player = False

    @property
    def width(self):  return TILE_SIZE
    @property
    def height(self): return TILE_SIZE

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def take_hit(self, damage=34):
        self.hp -= damage
        self.hit_flash_timer = 0.15
        if self.hp <= 0:
            self.alive = False
            return
        self.flee_timer = 3.0

    def _pick_direction(self):
        if self.rng.random () < 0.35:
            self.direction = (0, 0)
            self.idle_timer = self.rng.uniform(0.8, 2.0)
        else:
            self.direction = self.rng.choice(DIRECTIONS[1:])
            self.move_timer = self.rng.uniform(1.0, 2.5)
            self.idle_timer = 0.0

    def update(self, dt, world, player_rect, wanted_level):
        if not self.alive:
            return
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt
        if self.contact_dmg_timer > 0:
            self.contact_dmg_timer -= dt
        if self.flee_timer > 0:
            self.flee_timer -= dt

        px, py = player_rect.centerx, player_rect.centery
        my_cx  = self.x + TILE_SIZE / 2
        my_cy  = self.y + TILE_SIZE / 2
        dist = ((my_cx - px)**2 + (my_cy - py)**2) ** 0.5

        agressive = self.is_cop or (wanted_level >= CHASE_WANTED and dist < CHASE_RANGE)

        if self.flee_timer > 0 and not self.is_cop:
            dx, dy = self._away_from(player_rect)
            speed = NPC_FLEE_SPEED
        elif agressive:
            dx = 1 if px > my_cx else (-1 if px < my_cx else 0)
            dy = 1 if py > my_cy else (-1 if py < my_cy else 0)
            if abs(px - my_cx) >= abs(py - my_cy):
                dy = 0
            else: 
                dx = 0
            speed = NPC_FLEE_SPEED  # chase at flee speed — feels threatening
        else:
            if self.idle_timer > 0:
                self.idle_timer -= dt
                dx, dy = (0, 0)
                
    def _away_from(self, player_rect):
        dx = self.x - player_rect.x
        dy = self.y - player_rect.y
        if dx == 0 and dy == 0:
            return self.rng.choice(DIRECTIONS[1:])
        if abs(dx) >= abs(dy):
            return (1 if dx > 0 else -1), 0
        else:
            return 0, (1 if dy > 0 else -1)

    def _update_animation(self, dt, moving):
        if not moving:
            self.current_frame = "stand"
            self.anim_timer    = 0.0
            return
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer    = 0.0
            self.current_frame = "walk" if self.current_frame == "stand" else "stand"

    def draw(self, surface, camera_x, camera_y):
        img = self.frames[self.current_frame]
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)
        if self.hit_flash_timer > 0:
            flashed = img.copy()
            flashed.fill(RED_FLASH, special_flags=pygame.BLEND_RGBA_MULT)
            img = flashed

        surface.blit(img, (self.x - camera_x, self.y - camera_y))