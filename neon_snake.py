#!/usr/bin/env python3
"""Neon Snake — colourful classic."""

import random
import sys

import pygame

CELL = 24
COLS, ROWS = 32, 22
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 56


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Snake — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 48, bold=True)

    def reset():
        snake = [(8, 10), (7, 10), (6, 10)]
        direction = (1, 0)
        pending = (1, 0)
        food = (20, 10)
        score = 0
        alive = True
        return snake, direction, pending, food, score, alive

    def place_food(snake):
        while True:
            p = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if p not in snake:
                return p

    snake, direction, pending, food, score, alive = reset()
    tick = 0
    speed = 7

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key in (pygame.K_r,) and not alive:
                    snake, direction, pending, food, score, alive = reset()
                    speed = 7
                mapping = {
                    pygame.K_UP: (0, -1),
                    pygame.K_w: (0, -1),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_s: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_a: (-1, 0),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_d: (1, 0),
                }
                if event.key in mapping:
                    nd = mapping[event.key]
                    if nd[0] != -direction[0] or nd[1] != -direction[1]:
                        pending = nd

        tick += 1
        if alive and tick >= max(3, 12 - speed):
            tick = 0
            direction = pending
            hx, hy = snake[0]
            nx, ny = hx + direction[0], hy + direction[1]
            if nx < 0 or ny < 0 or nx >= COLS or ny >= ROWS or (nx, ny) in snake:
                alive = False
            else:
                snake.insert(0, (nx, ny))
                if (nx, ny) == food:
                    score += 10
                    speed = min(10, 7 + score // 50)
                    food = place_food(snake)
                else:
                    snake.pop()

        screen.fill((8, 10, 24))
        pygame.draw.rect(screen, (16, 20, 40), (0, 0, WIDTH, 56))
        screen.blit(font.render(f"NEON SNAKE    SCORE  {score}", True, (140, 255, 210)), (16, 16))
        screen.blit(font.render("x.com/ElbowOS", True, (180, 160, 255)), (WIDTH - 190, 16))

        for y in range(ROWS):
            for x in range(COLS):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, (14, 16, 34), (x * CELL, 56 + y * CELL, CELL, CELL))

        fx, fy = food
        pygame.draw.rect(
            screen,
            (255, 70, 140),
            (fx * CELL + 3, 56 + fy * CELL + 3, CELL - 6, CELL - 6),
            border_radius=6,
        )

        for i, (x, y) in enumerate(snake):
            t = i / max(1, len(snake))
            color = (int(40 + 80 * t), int(255 - 80 * t), int(180 + 40 * (1 - t)))
            pygame.draw.rect(
                screen,
                color,
                (x * CELL + 1, 56 + y * CELL + 1, CELL - 2, CELL - 2),
                border_radius=6,
            )

        if not alive:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            msg = big.render("GAME OVER", True, (255, 90, 120))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 16)))
            tip = font.render("Press R to restart", True, (240, 240, 255))
            screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
