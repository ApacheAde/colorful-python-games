#!/usr/bin/env python3
"""Color Stack — falling-block puzzle with a neon palette."""

import random
import sys

import pygame

COLS, ROWS = 10, 20
SIZE = 28
OX, OY = 40, 40
WIDTH, HEIGHT = 620, 640

SHAPES = {
    "I": [[(0, 1), (1, 1), (2, 1), (3, 1)], [(2, 0), (2, 1), (2, 2), (2, 3)]],
    "O": [[(1, 0), (2, 0), (1, 1), (2, 1)]],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [[(1, 0), (2, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1), (2, 2)]],
    "Z": [[(0, 0), (1, 0), (1, 1), (2, 1)], [(2, 0), (1, 1), (2, 1), (1, 2)]],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}
COLORS = {
    "I": (80, 220, 255),
    "O": (255, 210, 60),
    "T": (200, 110, 255),
    "S": (80, 230, 120),
    "Z": (255, 80, 110),
    "J": (80, 120, 255),
    "L": (255, 150, 50),
}


def collide(grid, name, rot, x, y):
    for cx, cy in SHAPES[name][rot % len(SHAPES[name])]:
        gx, gy = x + cx, y + cy
        if gx < 0 or gx >= COLS or gy >= ROWS:
            return True
        if gy >= 0 and grid[gy][gx]:
            return True
    return False


def place(grid, name, rot, x, y):
    for cx, cy in SHAPES[name][rot % len(SHAPES[name])]:
        gx, gy = x + cx, y + cy
        if 0 <= gy < ROWS:
            grid[gy][gx] = COLORS[name]


def clear_rows(grid):
    kept = [row for row in grid if any(c == 0 for c in row)]
    cleared = ROWS - len(kept)
    while len(kept) < ROWS:
        kept.insert(0, [0] * COLS)
    return kept, cleared


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Stack — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 42, bold=True)

    grid = [[0] * COLS for _ in range(ROWS)]
    bag = list(SHAPES)
    random.shuffle(bag)
    name = bag.pop()
    rot = 0
    x, y = 3, 0
    fall = 0
    speed = 36
    score = 0
    lines = 0
    over = False

    while True:
        move_x = 0
        hard = False
        rot_n = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_r and over:
                    return main()
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_x = -1
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_x = 1
                if event.key in (pygame.K_UP, pygame.K_w):
                    rot_n = 1
                if event.key == pygame.K_SPACE:
                    hard = True

        keys = pygame.key.get_pressed()
        soft = keys[pygame.K_DOWN] or keys[pygame.K_s]

        if not over:
            if move_x and not collide(grid, name, rot, x + move_x, y):
                x += move_x
            if rot_n and not collide(grid, name, rot + 1, x, y):
                rot += 1
            if hard:
                while not collide(grid, name, rot, x, y + 1):
                    y += 1
                fall = speed
            fall += 2 if soft else 1
            if fall >= speed:
                fall = 0
                if not collide(grid, name, rot, x, y + 1):
                    y += 1
                else:
                    place(grid, name, rot, x, y)
                    grid, cleared = clear_rows(grid)
                    if cleared:
                        score += (0, 100, 300, 500, 800)[cleared]
                        lines += cleared
                        speed = max(10, 36 - lines // 4)
                    if not bag:
                        bag = list(SHAPES)
                        random.shuffle(bag)
                    name = bag.pop()
                    rot, x, y = 0, 3, 0
                    if collide(grid, name, rot, x, y):
                        over = True

        screen.fill((14, 12, 28))
        pygame.draw.rect(screen, (30, 24, 55), (OX - 6, OY - 6, COLS * SIZE + 12, ROWS * SIZE + 12), border_radius=8)
        for r in range(ROWS):
            for c in range(COLS):
                cell = grid[r][c]
                rect = pygame.Rect(OX + c * SIZE, OY + r * SIZE, SIZE - 1, SIZE - 1)
                pygame.draw.rect(screen, cell if cell else (24, 20, 40), rect, border_radius=3)

        if not over:
            for cx, cy in SHAPES[name][rot % len(SHAPES[name])]:
                gx, gy = x + cx, y + cy
                if gy >= 0:
                    rect = pygame.Rect(OX + gx * SIZE, OY + gy * SIZE, SIZE - 1, SIZE - 1)
                    pygame.draw.rect(screen, COLORS[name], rect, border_radius=3)

        hud_x = OX + COLS * SIZE + 30
        screen.blit(font.render("COLOR STACK", True, (255, 220, 90)), (hud_x, 40))
        screen.blit(font.render(f"SCORE {score}", True, (240, 240, 255)), (hud_x, 90))
        screen.blit(font.render(f"LINES {lines}", True, (180, 220, 255)), (hud_x, 122))
        screen.blit(font.render("Arrows / WASD", True, (160, 160, 190)), (hud_x, 180))
        screen.blit(font.render("Up rotate", True, (160, 160, 190)), (hud_x, 206))
        screen.blit(font.render("Space drop", True, (160, 160, 190)), (hud_x, 232))
        screen.blit(font.render("x.com/ElbowOS", True, (200, 160, 255)), (hud_x, 300))
        if over:
            screen.blit(big.render("TOP OUT", True, (255, 80, 110)), (hud_x, 360))
            screen.blit(font.render("Press R", True, (255, 255, 255)), (hud_x, 410))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
