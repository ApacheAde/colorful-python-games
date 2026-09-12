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
    ("6", "Neon Roulette", "Spin the wheel", "neon_roulette.py", (255, 80, 160)),
    ("7", "Ruby Draw Poker", "5-card draw", "ruby_draw_poker.py", (200, 50, 80)),
    ("8", "Brick Breakout", "Smash the wall", "brick_breakout.py", (80, 200, 255)),
    ("9", "Pipe Glide", "Fly the gap", "pipe_glide.py", (80, 220, 90)),
    ("a", "Space Raiders", "Invader shooter", "space_raiders.py", (80, 220, 255)),
    ("b", "Neon Pong", "Rally vs CPU", "neon_pong.py", (80, 255, 200)),
    ("c", "Color Connect", "Four in a row", "color_connect.py", (240, 80, 90)),
    ("d", "Neon Craps", "Pass-line dice", "neon_craps.py", (120, 220, 90)),
    ("e", "Color Stack", "Falling blocks", "color_stack.py", (200, 120, 255)),
]


def run_game(filename: str) -> None:
    path = ROOT / filename
    subprocess.run([sys.executable, str(path)], check=False)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((980, 720))
    pygame.display.set_caption("ElbowOS Arcade — Colorful Python Games")
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("arial", 40, bold=True)
    item_font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 15)
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
                        if event.unicode.lower() == key:
                            run_game(filename)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        screen.fill((12, 16, 32))
        for i in range(24):
            shade = 18 + i * 3
            pygame.draw.rect(screen, (shade, 12, 40 + i * 2), (0, i * 32, 980, 32))

        title = title_font.render("ELBOWOS ARCADE", True, (255, 230, 120))
        screen.blit(title, title.get_rect(center=(490, 42)))
        sub = small.render("Full-colour Python 3 games  ·  https://x.com/ElbowOS", True, (200, 210, 230))
        screen.blit(sub, sub.get_rect(center=(490, 78)))

        hover_file = None
        for i, (key, name, blurb, filename, color) in enumerate(GAMES):
            col, row = i % 2, i // 2
            rect = pygame.Rect(40 + col * 470, 108 + row * 76, 440, 66)
            hot = rect.collidepoint(mx, my)
            bg = tuple(min(255, c + 40) for c in color) if hot else color
            pygame.draw.rect(screen, bg, rect, border_radius=14)
            pygame.draw.rect(screen, (20, 20, 30), rect.inflate(-8, -8), border_radius=10)
            label = item_font.render(f"{key}  {name}", True, bg)
            screen.blit(label, (rect.x + 22, rect.y + 10))
            desc = small.render(blurb, True, (210, 215, 230))
            screen.blit(desc, (rect.x + 48, rect.y + 38))
            if hot and clicked:
                hover_file = filename

        foot = hint.render("Click a game or press 1–9 / a–e   ·   Esc to quit", True, (160, 170, 190))
        screen.blit(foot, foot.get_rect(center=(490, 690)))
        pygame.display.flip()
        clock.tick(60)

        if hover_file:
            run_game(hover_file)

    pygame.quit()


if __name__ == "__main__":
    main()
