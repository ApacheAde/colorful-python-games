#!/usr/bin/env python3
"""Lucky Slots — colourful three-reel casino game."""

import random
import sys

import pygame

SYMBOLS = [
    ("CHERRY", (255, 70, 90), "●"),
    ("LEMON", (255, 220, 50), "◆"),
    ("BELL", (255, 190, 60), "▲"),
    ("STAR", (120, 200, 255), "★"),
    ("SEVEN", (255, 40, 60), "7"),
    ("DIAMOND", (180, 120, 255), "♦"),
]

PAYS = {
    "CHERRY": 4,
    "LEMON": 6,
    "BELL": 8,
    "STAR": 12,
    "SEVEN": 20,
    "DIAMOND": 30,
}


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((840, 620))
    pygame.display.set_caption("Lucky Slots — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title_f = pygame.font.SysFont("arial", 44, bold=True)
    font = pygame.font.SysFont("arial", 26, bold=True)
    huge = pygame.font.SysFont("arial", 64, bold=True)
    small = pygame.font.SysFont("arial", 18)

    credits = 200
    bet = 10
    reels = [0, 2, 4]
    spinning = 0
    offsets = [0, 0, 0]
    speeds = [0, 0, 0]
    message = "Press SPACE or click SPIN"
    last_win = 0

    spin_rect = pygame.Rect(310, 500, 220, 64)

    def start_spin():
        nonlocal spinning, credits, message, last_win, speeds, offsets
        if spinning or credits < bet:
            if credits < bet:
                message = "Not enough credits"
            return
        credits -= bet
        last_win = 0
        spinning = 90
        speeds[:] = [18, 22, 26]
        offsets[:] = [0, 0, 0]
        message = "Good luck..."

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_SPACE:
                    start_spin()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if spin_rect.collidepoint(event.pos):
                    start_spin()

        if spinning:
            spinning -= 1
            for i in range(3):
                offsets[i] += speeds[i]
                if offsets[i] >= 140:
                    offsets[i] = 0
                    reels[i] = (reels[i] + 1) % len(SYMBOLS)
                    if spinning < 30 + i * 12:
                        speeds[i] = max(0, speeds[i] - 2)
            if spinning == 0:
                speeds[:] = [0, 0, 0]
                offsets[:] = [0, 0, 0]
                names = [SYMBOLS[r][0] for r in reels]
                if names[0] == names[1] == names[2]:
                    last_win = bet * PAYS[names[0]]
                    credits += last_win
                    message = f"JACKPOT! Three {names[0]}  +{last_win}"
                elif names[0] == names[1] or names[1] == names[2] or names[0] == names[2]:
                    last_win = bet * 2
                    credits += last_win
                    message = f"Pair pays  +{last_win}"
                else:
                    message = "No luck — spin again"

        screen.fill((18, 10, 28))
        pygame.draw.rect(screen, (160, 30, 50), (40, 20, 760, 580), border_radius=28)
        pygame.draw.rect(screen, (40, 16, 30), (60, 90, 720, 390), border_radius=18)
        screen.blit(title_f.render("LUCKY SLOTS", True, (255, 220, 80)), (70, 32))
        screen.blit(small.render("x.com/ElbowOS", True, (255, 210, 180)), (640, 48))

        window = pygame.Rect(100, 120, 640, 240)
        pygame.draw.rect(screen, (10, 10, 18), window, border_radius=8)
        for i in range(3):
            col = pygame.Rect(120 + i * 210, 130, 190, 220)
            pygame.draw.rect(screen, (28, 22, 48), col, border_radius=10)
            idx = reels[i]
            name, color, glyph = SYMBOLS[idx]
            g = huge.render(glyph, True, color)
            screen.blit(g, g.get_rect(center=(col.centerx, col.centery - 16)))
            n = font.render(name, True, color)
            screen.blit(n, n.get_rect(center=(col.centerx, col.centery + 50)))

        pygame.draw.rect(screen, (255, 215, 70), window, 4, border_radius=8)

        screen.blit(font.render(f"CREDITS  {credits}", True, (255, 240, 200)), (100, 380))
        screen.blit(font.render(f"BET  {bet}", True, (255, 240, 200)), (380, 380))
        screen.blit(font.render(f"WIN  {last_win}", True, (120, 255, 160)), (560, 380))
        screen.blit(small.render(message, True, (255, 230, 180)), (100, 420))
        screen.blit(small.render("Pays: pair x2  ·  three-of-a-kind  cherry 4x … diamond 30x", True, (220, 190, 160)), (100, 452))

        hover = spin_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (255, 210, 50) if hover else (240, 170, 30), spin_rect, border_radius=14)
        spin_txt = font.render("SPIN", True, (40, 20, 10))
        screen.blit(spin_txt, spin_txt.get_rect(center=spin_rect.center))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
