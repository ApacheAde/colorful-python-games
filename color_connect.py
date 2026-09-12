#!/usr/bin/env python3
"""Color Connect — four-in-a-row vs a simple CPU."""

import random
import sys

import pygame

COLS, ROWS = 7, 6
CELL = 78
PAD = 40
WIDTH = PAD * 2 + COLS * CELL
HEIGHT = PAD * 2 + (ROWS + 1) * CELL + 40
RED = (240, 70, 80)
YEL = (255, 210, 50)


def winner(grid):
    dirs = ((1, 0), (0, 1), (1, 1), (1, -1))
    for r in range(ROWS):
        for c in range(COLS):
            p = grid[r][c]
            if not p:
                continue
            for dc, dr in dirs:
                ok = True
                for i in range(4):
                    cc, rr = c + dc * i, r + dr * i
                    if not (0 <= cc < COLS and 0 <= rr < ROWS) or grid[rr][cc] != p:
                        ok = False
                        break
                if ok:
                    return p
    return 0


def drop(grid, col, piece):
    for r in range(ROWS - 1, -1, -1):
        if grid[r][col] == 0:
            grid[r][col] = piece
            return True
    return False


def cpu_move(grid):
    opens = [c for c in range(COLS) if grid[0][c] == 0]
    if not opens:
        return None
    for piece in (2, 1):
        for c in opens:
            trial = [row[:] for row in grid]
            drop(trial, c, piece)
            if winner(trial) == piece:
                return c
    return random.choice(opens)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Connect — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24, bold=True)
    big = pygame.font.SysFont("arial", 40, bold=True)

    grid = [[0] * COLS for _ in range(ROWS)]
    turn = 1
    result = 0
    hover = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_r:
                    grid = [[0] * COLS for _ in range(ROWS)]
                    turn, result = 1, 0
            if event.type == pygame.MOUSEMOTION:
                hover = max(0, min(COLS - 1, (event.pos[0] - PAD) // CELL))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and result == 0 and turn == 1:
                if drop(grid, hover, 1):
                    result = winner(grid)
                    turn = 2

        if result == 0 and turn == 2:
            pygame.time.delay(180)
            col = cpu_move(grid)
            if col is not None:
                drop(grid, col, 2)
                result = winner(grid)
            turn = 1
            if all(grid[0][c] for c in range(COLS)) and result == 0:
                result = 3

        screen.fill((16, 28, 70))
        board = pygame.Rect(PAD - 10, PAD + CELL - 10, COLS * CELL + 20, ROWS * CELL + 20)
        pygame.draw.rect(screen, (30, 90, 180), board, border_radius=18)

        ghost_y = PAD + CELL // 2
        pygame.draw.circle(screen, RED if turn == 1 else YEL, (PAD + hover * CELL + CELL // 2, ghost_y), 28)

        for r in range(ROWS):
            for c in range(COLS):
                cx = PAD + c * CELL + CELL // 2
                cy = PAD + CELL + r * CELL + CELL // 2
                val = grid[r][c]
                color = (12, 20, 40) if val == 0 else (RED if val == 1 else YEL)
                pygame.draw.circle(screen, color, (cx, cy), 30)
                pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 30, 2)

        if result == 1:
            text, color = "YOU WIN", RED
        elif result == 2:
            text, color = "CPU WINS", YEL
        elif result == 3:
            text, color = "DRAW", (200, 200, 220)
        else:
            text, color = "Your drop — click a column", (220, 230, 255)
        screen.blit(big.render(text, True, color), (PAD, 8))
        screen.blit(font.render("R restart   Esc quit   x.com/ElbowOS", True, (180, 200, 230)), (PAD, HEIGHT - 36))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
