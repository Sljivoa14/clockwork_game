"""
cop.py file
-
COP NPC behavior. cop appears when we did crimes (hurt npcs, and more will be added).
"""

import pygame
from npc import NPC
from settings import (
    TILE_SIZE,
    COP_SPEED,
    COP_CHASE_RANGE,
    COP_CONTACT_DAMAGE_CD,

)

class Cop(NPC):
    def __init__(self, x, y, sprite_path, rng):
        super().__init__(x, y, sprite_path, rng)
        self.is_cop = True
        self.speed = COP_SPEED
        self.chase_range = COP_CHASE_RANGE
        self.contact_damage_cd  = COP_CONTACT_DAMAGE_CD

    def update(self, dt, world, player_rect, wanted_level):
        if not self.alive:
            return
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt
        if self.contact_dmg_timer > 0:
            self.contact_dmg_timer -= dt

        px, py = player_rect.centerx, player_rect.centery
        my_cx = self.x + TILE_SIZE / 2
        my_cy = self.y + TILE_SIZE / 2
        dist = ((my_cx - px)**2 + (my_cy - py)**2) ** 0.5 
        chasing = wanted_level > 0 or dist < self.chase_range

        if chasing:
            dx = 1 if px > my_cx else (-1 if px < my_cx else 0)
            dy = 1 if py > my_cy else (-1 if py < my_cy else 0)
            if abs(px - my_cx) >= abs(py - my_cy):
                dy = 0
            else:
                dx = 0
            speed = self.speed
        else:
            self.move_timer  -= dt
            if self.move_timer <= 0:
                self._pick_direction()
            dx, dy = self.direction
            speed = self.speed * 0.5


        moving = (dx, dy) != (0, 0)
        if dx < 0:
            self.facing_left = True
        elif dx > 0:
            self.facing_left = False

        if dx != 0:
            r = pygame.Rect(int(self.x + dx), int(self.y), self.width, self.height)
            if not world.rect_collides(r): 
                self.x += dx * speed
            else:
                self._pick_direction()

        if dy != 0:
            r = pygame.Rect(int(self.x), int(self.y + dy * speed), self.width, self.height)
            if not world.rect_collides(r):
                self.y += dy * speed
            else:
                self._pick_direction()

        if chasing and self.contact_dmg_timer <= 0  and self.get_rect().colliderect(player_rect):
            self.contact_dmg_timer = self.contact_damage_cd
            self._wants_to_damage_player = True
        else:
            self._wants_to_damage_player = False

        self._update_animation(dt, moving)

    def take_hit(self, damage = 34):
        self.hp -= damage
        self.hit_flash_timer = 0.15
        if self.hp <= 0:
            self.alive = False


