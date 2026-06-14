"""
main.py
-------
The entry point. This is where the actual "game loop" lives:

    while running:
        1. handle input/events
        2. update game state
        3. draw everything

Run with:
    python main.py
"""

import pygame
from settings import (
    RENDER_WIDTH, RENDER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    FPS, BLACK, TILE_SIZE,
)
from world import World
from player import Player


def compute_camera(player, world):
    """
    Work out the top-left world-pixel coordinate the camera should
    show, so the player stays centered on screen - but clamp it so
    the camera never shows past the edges of the map.
    """
    cam_x = player.x + TILE_SIZE / 2 - RENDER_WIDTH / 2
    cam_y = player.y + TILE_SIZE / 2 - RENDER_HEIGHT / 2

    max_cam_x = world.pixel_width() - RENDER_WIDTH
    max_cam_y = world.pixel_height() - RENDER_HEIGHT

    cam_x = max(0, min(cam_x, max_cam_x))
    cam_y = max(0, min(cam_y, max_cam_y))
    return cam_x, cam_y


def main():
    pygame.init()
    pygame.display.set_caption("Pixel City - Prototype")

    # The real window the player sees.
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # We draw everything onto this small surface first (native pixel art
    # resolution), then scale it up to fill the window. This is what
    # gives the "chunky retro pixel" look.
    render_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))

    clock = pygame.time.Clock()

    world = World()

    # Spawn the player roughly in the middle of the map.
    spawn_x = world.pixel_width() / 2
    spawn_y = world.pixel_height() / 2
    player = Player(spawn_x, spawn_y)

    running = True
    while running:
        # dt = "delta time" - seconds since the last frame. Using this
        # for animation timing keeps speed consistent even if the
        # framerate isn't perfectly steady.
        dt = clock.tick(FPS) / 1000.0

        # --- 1. Handle events (things that happen once, like key presses) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- 2. Update game state ---
        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt, world)
        camera_x, camera_y = compute_camera(player, world)

        # --- 3. Draw everything ---
        render_surface.fill(BLACK)
        world.draw(render_surface, camera_x, camera_y)
        player.draw(render_surface, camera_x, camera_y)

        # Scale the small render surface up to the window size.
        # NEAREST scaling keeps the pixels sharp/blocky instead of blurry.
        scaled = pygame.transform.scale(render_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
