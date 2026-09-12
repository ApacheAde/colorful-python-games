#!/usr/bin/env python3
"""Memory Cards — colourful flip-and-match."""

import random
import sys

import pygame

COLORS = [
    ((255, 80, 80), "RED"),
    ((80, 200, 90), "GREEN"),
    ((70, 140, 255), "BLUE"),
    ((255, 210, 50), "YELLOW"),
    ((220, 90, 220), "PURPLE"),
    ((255, 140, 50), "ORANGE"),
    ((80, 230, 230), "CYAN"),
    ((255, 120, 170), "PINK"),
]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((880, 640))
    pygame.display.set_caption("Memory Cards — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title_f = pygame.font.SysFont("arial", 36, bold=True)
    font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 16)

    def deal():
        deck = COLORS * 2
        random.shuffle(deck)
        cards = []
        for i, (color, name) in enumerate(deck):
            r, c = divmod(i, 4)
            rect = pygame.Rect(80 + c * 190, 110 + r * 120, 170, 104)
            cards.append({"rect": rect, "color": color, "name": name, "up": False, "gone": False})
        return cards

    cards = deal()
    picked: list[int] = []
    freeze = 0
    moves = 0
    matched = 0

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
                    cards = deal()
                    picked = []
                    freeze = 0
                    moves = 0
                    matched = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and freeze == 0:
                if matched == 8:
                    cards = deal()
                    picked = []
                    moves = 0
                    matched = 0
                    continue
                pos = event.pos
                for i, card in enumerate(cards):
                    if card["gone"] or card["up"]:
                        continue
                    if card["rect"].collidepoint(pos) and len(picked) < 2:
                        card["up"] = True
                        picked.append(i)
                if len(picked) == 2:
                    moves += 1
                    a, b = cards[picked[0]], cards[picked[1]]
                    if a["name"] == b["name"]:
                        a["gone"] = b["gone"] = True
                        matched += 1
                        picked = []
                    else:
                        freeze = 45

        if freeze:
            freeze -= 1
            if freeze == 0:
                for i in picked:
                    cards[i]["up"] = False
                picked = []

        screen.fill((24, 28, 56))
        pygame.draw.rect(screen, (36, 42, 80), (30, 20, 820, 600), border_radius=20)
        screen.blit(title_f.render("MEMORY CARDS", True, (255, 230, 120)), (50, 36))
        screen.blit(font.render(f"Moves {moves}   Matches {matched}/8", True, (220, 230, 255)), (50, 78))
        screen.blit(small.render("x.com/ElbowOS   ·   R to restart", True, (180, 190, 220)), (560, 48))

        mx, my = pygame.mouse.get_pos()
        for card in cards:
            r = card["rect"]
            if card["gone"]:
                pygame.draw.rect(screen, (28, 34, 64), r, border_radius=12)
                continue
            hot = r.collidepoint(mx, my)
            if card["up"]:
                pygame.draw.rect(screen, card["color"], r, border_radius=12)
                label = font.render(card["name"], True, (20, 20, 30))
                screen.blit(label, label.get_rect(center=r.center))
            else:
                bg = (90, 110, 210) if hot else (70, 90, 190)
                pygame.draw.rect(screen, bg, r, border_radius=12)
                pygame.draw.rect(screen, (160, 180, 255), r, 3, border_radius=12)
                q = font.render("?", True, (240, 245, 255))
                screen.blit(q, q.get_rect(center=r.center))

        if matched == 8:
            banner = pygame.Rect(140, 280, 600, 90)
            pygame.draw.rect(screen, (255, 210, 70), banner, border_radius=16)
            msg = title_f.render(f"Cleared in {moves} moves!", True, (40, 30, 10))
            screen.blit(msg, msg.get_rect(center=banner.center))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
