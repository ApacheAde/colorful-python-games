#!/usr/bin/env python3
"""Neon Craps — pass-line dice table in full colour."""

import random
import sys

import pygame

WIDTH, HEIGHT = 900, 560


def roll():
    return random.randint(1, 6), random.randint(1, 6)


def draw_die(surf, x, y, n, color):
    pygame.draw.rect(surf, color, (x, y, 70, 70), border_radius=10)
    pygame.draw.rect(surf, (20, 20, 30), (x, y, 70, 70), 3, border_radius=10)
    spots = {
        1: [(35, 35)],
        2: [(18, 18), (52, 52)],
        3: [(18, 18), (35, 35), (52, 52)],
        4: [(18, 18), (52, 18), (18, 52), (52, 52)],
        5: [(18, 18), (52, 18), (35, 35), (18, 52), (52, 52)],
        6: [(18, 18), (52, 18), (18, 35), (52, 35), (18, 52), (52, 52)],
    }
    for sx, sy in spots[n]:
        pygame.draw.circle(surf, (20, 20, 30), (x + sx, y + sy), 6)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Craps — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 36, bold=True)
    huge = pygame.font.SysFont("arial", 52, bold=True)

    bank = 200
    stake = 10
    point = 0
    dice = (1, 1)
    message = "Pass-line bet. Space to roll."
    flash = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    stake = min(bank, stake + 5)
                if event.key == pygame.K_MINUS:
                    stake = max(5, stake - 5)
                if event.key == pygame.K_SPACE and bank >= stake:
                    a, b = roll()
                    dice = (a, b)
                    total = a + b
                    if point == 0:
                        if total in (7, 11):
                            bank += stake
                            flash = f"NATURAL {total}  +${stake}"
                        elif total in (2, 3, 12):
                            bank -= stake
                            flash = f"CRAPS {total}  -${stake}"
                        else:
                            point = total
                            flash = f"POINT is {point}"
                    else:
                        if total == point:
                            bank += stake
                            flash = f"HIT {point}  +${stake}"
                            point = 0
                        elif total == 7:
                            bank -= stake
                            flash = f"SEVEN-OUT  -${stake}"
                            point = 0
                        else:
                            flash = f"Rolled {total} — point {point}"
                    if bank < stake:
                        stake = max(5, bank if bank else 5)
                    message = "Come-out roll." if point == 0 else f"Shooting for point {point}."

        screen.fill((12, 60, 36))
        pygame.draw.rect(screen, (8, 40, 24), (30, 30, WIDTH - 60, HEIGHT - 60), border_radius=24)
        pygame.draw.rect(screen, (220, 190, 80), (30, 30, WIDTH - 60, HEIGHT - 60), 4, border_radius=24)

        screen.blit(huge.render("NEON CRAPS", True, (255, 220, 90)), (60, 50))
        screen.blit(font.render("x.com/ElbowOS", True, (180, 220, 160)), (WIDTH - 240, 60))

        screen.blit(big.render(f"BANK  ${bank}", True, (120, 255, 180)), (60, 120))
        screen.blit(big.render(f"STAKE ${stake}", True, (255, 210, 90)), (60, 168))
        screen.blit(big.render(f"POINT {point or '—'}", True, (255, 140, 90)), (60, 216))
        screen.blit(font.render(message, True, (230, 240, 220)), (60, 270))
        screen.blit(big.render(flash, True, (255, 240, 140)), (60, 310))

        draw_die(screen, 620, 150, dice[0], (250, 245, 230))
        draw_die(screen, 710, 150, dice[1], (250, 245, 230))
        screen.blit(huge.render(str(sum(dice)), True, (255, 230, 80)), (670, 240))

        tip = "SPACE roll    + / - stake    Esc quit"
        screen.blit(font.render(tip, True, (200, 220, 190)), (60, HEIGHT - 90))
        if bank <= 0:
            screen.blit(big.render("BUSTED — restart the game", True, (255, 90, 90)), (60, 380))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
