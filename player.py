"""
player.py
---------
Player: movement, sword attack, gun + bullets, health tracking.
"""

import pygame
from settings import (
    TILE_SIZE, PLAYER_SPEED,
    ATTACK_DURATION, ATTACK_COOLDOWN, ATTACK_REACH_MELEE,
    PLAYER_MAX_HP,
)

from bullet import Bullet

GUN_COOLDOWN = 0.25

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        # --- Sprites ---
        sheet = pygame.image.load("assets/player.png").convert_alpha()
        self.frames = {
            "stand": sheet.subsurface(pygame.Rect(0, 0,         TILE_SIZE, TILE_SIZE)),
            "walk":  sheet.subsurface(pygame.Rect(0, TILE_SIZE, TILE_SIZE, TILE_SIZE)),
        }
        self.gun_image   = pygame.image.load("assets/gun.png").convert_alpha()
        self.sword_image = pygame.image.load("assets/sword.png").convert_alpha()

        # --- State ---
        self.facing      = "right"
        self.facing_left = False
        self.current_frame = "stand"
        self.anim_timer    = 0.0
        self.anim_speed    = 0.12

        # --- Health ---
        self.hp     = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.alive  = True

        # --- Weapons ---
        # weapon: "sword" or "gun"
        self.weapon = "sword"

        # Sword timers
        self.attack_timer          = 0.0
        self.attack_cooldown_timer = 0.0

        # Gun timers + bullet list
        self.gun_cooldown_timer = 0.0
        self.bullets = []          # list of Bullet objects owned by the player

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def width(self):  return TILE_SIZE

    @property
    def height(self): return TILE_SIZE

    @property
    def is_attacking(self):
        return self.weapon == "sword" and self.attack_timer > 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)

    # ── Input & update ─────────────────────────────────────────────────────────

    def handle_input(self, keys, dt, world):
        dx = dy = 0.0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += PLAYER_SPEED
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= PLAYER_SPEED
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += PLAYER_SPEED

        moving = dx != 0 or dy != 0

        # Update facing
        if dx < 0:   self.facing = "left";  self.facing_left = True
        elif dx > 0: self.facing = "right"; self.facing_left = False
        elif dy < 0: self.facing = "up"
        elif dy > 0: self.facing = "down"

        # Weapon switch: 1 = sword, 2 = gun
        if keys[pygame.K_1]: self.weapon = "sword"
        if keys[pygame.K_2]: self.weapon = "gun"

        # Move X
        if dx != 0:
            r = pygame.Rect(int(self.x + dx), int(self.y), self.width, self.height)
            if not world.rect_collides(r): self.x += dx

        # Move Y
        if dy != 0:
            r = pygame.Rect(int(self.x), int(self.y + dy), self.width, self.height)
            if not world.rect_collides(r): self.y += dy

        self._update_animation(dt, moving)

        # Tick attack timers
        if self.attack_timer > 0:          self.attack_timer          -= dt
        if self.attack_cooldown_timer > 0: self.attack_cooldown_timer -= dt
        if self.gun_cooldown_timer > 0:    self.gun_cooldown_timer    -= dt

        # Update bullets
        for b in self.bullets:
            b.update(world)
        self.bullets = [b for b in self.bullets if b.alive]

    def try_attack(self):
        """SPACE — sword swing. Returns True if the swing started."""
        if self.weapon != "sword":
            return False
        if self.attack_cooldown_timer <= 0:
            self.attack_timer          = ATTACK_DURATION
            self.attack_cooldown_timer = ATTACK_COOLDOWN
            return True
        return False

    def try_shoot(self):
        """F or left-click — fire a bullet. Returns the Bullet or None."""
        if self.weapon != "gun":
            return None
        if self.gun_cooldown_timer <= 0:
            cx, cy = self.center()
            b = Bullet(cx, cy, self.facing)
            self.bullets.append(b)
            self.gun_cooldown_timer = GUN_COOLDOWN
            return b
        return None

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False

    def get_attack_rect(self):
        rect = self.get_rect()
        if self.facing == "left":
            return pygame.Rect(rect.left - ATTACK_REACH_MELEE, rect.top,
                               ATTACK_REACH_MELEE + rect.w // 2, rect.h)
        elif self.facing == "right":
            return pygame.Rect(rect.right - rect.w // 2, rect.top,
                               ATTACK_REACH_MELEE + rect.w // 2, rect.h)
        elif self.facing == "up":
            return pygame.Rect(rect.left, rect.top - ATTACK_REACH_MELEE,
                               rect.w, ATTACK_REACH_MELEE + rect.h // 2)
        else:
            return pygame.Rect(rect.left, rect.bottom - rect.h // 2,
                               rect.w, ATTACK_REACH_MELEE + rect.h // 2)

    # ── Animation ──────────────────────────────────────────────────────────────

    def _update_animation(self, dt, moving):
        if not moving:
            self.current_frame = "stand"
            self.anim_timer = 0.0
            return
        self.anim_timer += dt

        if self.anim_timer >= self.anim_speed:
            self.anim_timer    = 0.0
            self.current_frame = "walk" if self.current_frame == "stand" else "stand"

    # ── Drawing ────────────────────────────────────────────────────────────────
    def draw (self, surface, camera_x, camera_y):
        img =  self.frames[self.current_frame]
        if self.facing_left:
            img = pygame.transform.flip (img, True, False)

        sx = self.x - camera_x
        sy = self.y - camera_y
        surface.blit(img, (sx, sy))

        if self.is_attacking:
            self._draw_sword(surface, sx, sy)
        elif self.weapon == "gun":
            self._draw_gun(surface, sx, sy)

        for b in self.bullets:
            b.draw(surface, camera_x, camera_y)

    def _draw_sword(self, surface, sx, sy):
        sword = self.sword_image
        offsets = {
            "up":    (pygame.transform.rotate(sword,   0), (sx,            sy - TILE_SIZE)),
            "down":  (pygame.transform.rotate(sword, 180), (sx,            sy + TILE_SIZE)),
            "left":  (pygame.transform.rotate(sword,  90), (sx - TILE_SIZE, sy)),
            "right": (pygame.transform.rotate(sword, -90), (sx + TILE_SIZE, sy)),
        }

    def _draw_gun(self, surface, sx, sy):
        gun = self.gun_image
        offsets = {
            "up":    (pygame.transform.rotate(gun,   90), (sx,                    sy - TILE_SIZE // 2)),
            "down":  (pygame.transform.rotate(gun,  -90), (sx,                    sy + TILE_SIZE // 2)),
            "left":  (pygame.transform.flip(gun, True, False), (sx - TILE_SIZE,   sy)),
            "right": (gun,                                      (sx + TILE_SIZE // 2, sy)),
        }
        rotated, pos = offsets[self.facing]
        surface.blit(rotated, pos)