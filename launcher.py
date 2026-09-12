#!/usr/bin/env python3
"""Full-colour game launcher for the ElbowOS arcade."""

import subprocess
import sys
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent

GAMES = [
    ("1", "Super Block Bros", "Platform jumper", "super_block_bros.py", (255, 92, 87)),
    ("2", "Neon Blackjack", "Casino cards", "neon_blackjack.py", (80, 220, 140)),
    ("3", "Lucky Slots", "Three-reel slots", "lucky_slots.py", (255, 200, 60)),
    ("4", "Memory Cards", "Flip & match", "memory_cards.py", (120, 170, 255)),
    ("5", "Neon Snake", "Eat, grow, glow", "neon_snake.py", (220, 110, 255)),
]


def run_game(filename: str) -> None:
    path = ROOT / filename
    subprocess.run([sys.executable, str(path)], check=False)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((900, 620))
    pygame.display.set_caption("ElbowOS Arcade — Colorful Python Games")
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("arial", 42, bold=True)
    item_font = pygame.font.SysFont("arial", 28, bold=True)
    small = pygame.font.SysFont("arial", 18)
    hint = pygame.font.SysFont("arial", 16)

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    for key, *_rest, filename, _c in GAMES:
                        if event.unicode == key:
                            run_game(filename)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        screen.fill((12, 16, 32))
        for i in range(18):
            shade = 18 + i * 4
            pygame.draw.rect(screen, (shade, 12, 40 + i * 2), (0, i * 36, 900, 36))

        title = title_font.render("ELBOWOS ARCADE", True, (255, 230, 120))
        screen.blit(title, title.get_rect(center=(450, 58)))
        sub = small.render("Full-colour Python 3 games  ·  x.com/ElbowOS", True, (200, 210, 230))
        screen.blit(sub, sub.get_rect(center=(450, 100)))

        hover_file = None
        for i, (key, name, blurb, filename, color) in enumerate(GAMES):
            rect = pygame.Rect(120, 140 + i * 80, 660, 68)
            hot = rect.collidepoint(mx, my)
            bg = tuple(min(255, c + 40) for c in color) if hot else color
            pygame.draw.rect(screen, bg, rect, border_radius=16)
            pygame.draw.rect(screen, (20, 20, 30), rect.inflate(-8, -8), border_radius=12)
            label = item_font.render(f"{key}  {name}", True, bg)
            screen.blit(label, (150, rect.y + 8))
            desc = small.render(blurb, True, (210, 215, 230))
            screen.blit(desc, (190, rect.y + 38))
            if hot and clicked:
                hover_file = filename

        foot = hint.render("Click a game or press 1–5   ·   Esc to quit", True, (160, 170, 190))
        screen.blit(foot, foot.get_rect(center=(450, 575)))
        pygame.display.flip()
        clock.tick(60)

        if hover_file:
            run_game(hover_file)

    pygame.quit()


if __name__ == "__main__":
    main()
