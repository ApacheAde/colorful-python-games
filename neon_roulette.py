#!/usr/bin/env python3
"""Neon Roulette — colourful European-style wheel. Original casino mini-game."""
from __future__ import annotations

import math
import random
import sys

import pygame

W, H = 960, 640
RED_SET = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
ORDER = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
    5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
]


def pocket_color(n: int) -> str:
    if n == 0:
        return "green"
    return "red" if n in RED_SET else "black"


def rgb(kind: str) -> tuple[int, int, int]:
    return {"green": (40, 180, 90), "red": (220, 50, 70), "black": (28, 28, 36)}[kind]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Roulette")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    big = pygame.font.SysFont("arial", 36, bold=True)
    small = pygame.font.SysFont("arial", 16)

    bank = 500
    bet = 10
    choice = "red"
    spinning = False
    angle = 0.0
    speed = 0.0
    result: int | None = None
    message = "Pick a colour and spin"
    flash = 0

    bets = [("red", "RED x2"), ("black", "BLACK x2"), ("green", "ZERO x14"), ("even", "EVEN x2"), ("odd", "ODD x2")]

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not spinning and bank >= bet:
                    spinning = True
                    speed = random.uniform(14.0, 20.0)
                    result = None
                    message = "Spinning..."
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    bet = min(100, bet + 5)
                elif event.key == pygame.K_MINUS:
                    bet = max(5, bet - 5)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not spinning:
                mx, my = event.pos
                for i, (key, _) in enumerate(bets):
                    rx, ry = 40 + i * 180, 560
                    if pygame.Rect(rx, ry, 170, 50).collidepoint(mx, my):
                        choice = key
                if pygame.Rect(760, 480, 160, 50).collidepoint(mx, my) and bank >= bet:
                    spinning = True
                    speed = random.uniform(14.0, 20.0)
                    result = None
                    message = "Spinning..."

        if spinning:
            angle += speed * dt * 60
            speed *= 0.985
            if speed < 0.15:
                spinning = False
                idx = int(((-angle) % 360) / (360 / 37)) % 37
                result = ORDER[idx]
                won = 0
                pc = pocket_color(result)
                if choice == "green" and result == 0:
                    won = bet * 14
                elif choice in ("red", "black") and pc == choice:
                    won = bet * 2
                elif choice == "even" and result != 0 and result % 2 == 0:
                    won = bet * 2
                elif choice == "odd" and result != 0 and result % 2 == 1:
                    won = bet * 2
                bank += won - bet
                message = f"Landed {result} ({pc.upper()})  —  {'WON +' + str(won - bet) if won else 'lost ' + str(bet)}"
                flash = 20

        screen.fill((12, 8, 24))
        pygame.draw.rect(screen, (28, 18, 48), (0, 0, W, 70))
        screen.blit(big.render("NEON ROULETTE", True, (255, 80, 180)), (20, 16))
        screen.blit(font.render(f"Bank ${bank}   Bet ${bet}   [+/-]", True, (240, 230, 120)), (520, 24))

        cx, cy, r = 480, 300, 210
        pygame.draw.circle(screen, (80, 60, 20), (cx, cy), r + 16)
        pygame.draw.circle(screen, (40, 30, 10), (cx, cy), r + 8)
        step = 360 / 37
        for i, n in enumerate(ORDER):
            a0 = math.radians(i * step + angle)
            a1 = math.radians((i + 1) * step + angle)
            pts = [(cx, cy)]
            for t in (a0, (a0 + a1) / 2, a1):
                pts.append((cx + math.cos(t) * r, cy + math.sin(t) * r))
            pygame.draw.polygon(screen, rgb(pocket_color(n)), pts)
        pygame.draw.circle(screen, (18, 12, 30), (cx, cy), 48)
        pygame.draw.polygon(screen, (255, 220, 80), [(cx, cy - r - 6), (cx - 10, cy - r + 18), (cx + 10, cy - r + 18)])

        if result is not None:
            col = rgb(pocket_color(result))
            glow = (min(255, col[0] + 40), min(255, col[1] + 40), min(255, col[2] + 40))
            screen.blit(big.render(str(result), True, glow), (cx - 18, cy - 18))

        color = (255, 240, 180) if flash % 2 == 0 else (255, 80, 160)
        if flash:
            flash -= 1
        screen.blit(font.render(message, True, color), (40, 500))

        for i, (key, label) in enumerate(bets):
            rx, ry = 40 + i * 180, 560
            active = choice == key
            bg = (90, 30, 80) if active else (40, 24, 56)
            pygame.draw.rect(screen, bg, (rx, ry, 170, 50), border_radius=10)
            pygame.draw.rect(screen, (255, 90, 200) if active else (90, 70, 120), (rx, ry, 170, 50), 2, border_radius=10)
            screen.blit(small.render(label, True, (255, 240, 250)), (rx + 18, ry + 16))

        pygame.draw.rect(screen, (200, 50, 120), (760, 480, 160, 50), border_radius=10)
        screen.blit(font.render("SPIN", True, (255, 255, 255)), (808, 492))
        screen.blit(small.render("Space to spin  ·  Esc quit", True, (160, 140, 180)), (760, 90))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
