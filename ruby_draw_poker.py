#!/usr/bin/env python3
"""Ruby Draw Poker — 5-card draw vs the house. Colourful card table."""
from __future__ import annotations

import random
import sys
from collections import Counter

import pygame

W, H = 960, 640
RANKS = "A23456789TJQK"
SUITS = ["\u2665", "\u2666", "\u2663", "\u2660"]
SUIT_COL = {"\u2665": (230, 50, 70), "\u2666": (230, 80, 40), "\u2663": (40, 160, 90), "\u2660": (40, 50, 90)}


def new_deck() -> list[str]:
    return [r + s for r in RANKS for s in SUITS]


def rank_val(card: str) -> int:
    return RANKS.index(card[0])


def hand_score(cards: list[str]) -> tuple[int, str]:
    ranks = sorted(rank_val(c) for c in cards)
    suits = [c[1] for c in cards]
    counts = Counter(ranks)
    freq = sorted(counts.values(), reverse=True)
    flush = len(set(suits)) == 1
    uniq = sorted(set(ranks))
    straight = len(uniq) == 5 and uniq[-1] - uniq[0] == 4
    wheel = set(ranks) == {0, 1, 2, 3, 12}
    if wheel:
        straight = True
    if straight and flush:
        return (8, "Straight Flush")
    if freq[0] == 4:
        return (7, "Four of a Kind")
    if freq == [3, 2]:
        return (6, "Full House")
    if flush:
        return (5, "Flush")
    if straight:
        return (4, "Straight")
    if freq[0] == 3:
        return (3, "Three of a Kind")
    if freq == [2, 2, 1]:
        return (2, "Two Pair")
    if freq[0] == 2:
        return (1, "One Pair")
    return (0, "High Card")


def draw_card(surf, font, big, card: str, x: int, y: int, held: bool) -> pygame.Rect:
    rect = pygame.Rect(x, y, 110, 154)
    pygame.draw.rect(surf, (250, 248, 240), rect, border_radius=10)
    border = (255, 210, 60) if held else (30, 20, 40)
    pygame.draw.rect(surf, border, rect, 4, border_radius=10)
    col = SUIT_COL[card[1]]
    label = card[0].replace("T", "10")
    surf.blit(big.render(label, True, col), (x + 10, y + 8))
    surf.blit(font.render(card[1], True, col), (x + 12, y + 50))
    surf.blit(big.render(card[1], True, col), (x + 38, y + 70))
    return rect


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Ruby Draw Poker")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    big = pygame.font.SysFont("arial", 36, bold=True)
    small = pygame.font.SysFont("arial", 16)

    bank = 500
    bet = 20
    deck: list[str] = []
    player: list[str] = []
    held = [False] * 5
    phase = "ready"
    msg = "Deal a hand — click cards to HOLD, then DRAW"
    last = ""

    def deal() -> None:
        nonlocal deck, player, held, phase, msg, bank
        if bank < bet:
            msg = "Not enough chips"
            return
        bank -= bet
        deck = new_deck()
        random.shuffle(deck)
        player = [deck.pop() for _ in range(5)]
        held = [False] * 5
        phase = "hold"
        msg = "Click cards to HOLD, then DRAW"

    def draw() -> None:
        nonlocal player, phase, msg, last, bank
        for i in range(5):
            if not held[i]:
                player[i] = deck.pop()
        score, name = hand_score(player)
        payouts = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 6, 6: 9, 7: 25, 8: 50}
        win = bet * payouts[score]
        bank += win
        last = name
        phase = "result"
        msg = f"{name}  —  {'won $' + str(win) if win else 'no payout'}"

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_d:
                    if phase in ("ready", "result"):
                        deal()
                    elif phase == "hold":
                        draw()
                elif event.key == pygame.K_EQUALS:
                    bet = min(100, bet + 5)
                elif event.key == pygame.K_MINUS:
                    bet = max(5, bet - 5)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if phase == "hold":
                    for i in range(5):
                        r = pygame.Rect(80 + i * 160, 240, 110, 154)
                        if r.collidepoint(mx, my):
                            held[i] = not held[i]
                if pygame.Rect(360, 520, 240, 52).collidepoint(mx, my):
                    if phase in ("ready", "result"):
                        deal()
                    elif phase == "hold":
                        draw()

        screen.fill((18, 8, 28))
        pygame.draw.rect(screen, (90, 16, 40), (0, 0, W, 80))
        screen.blit(big.render("RUBY DRAW POKER", True, (255, 210, 80)), (24, 20))
        screen.blit(font.render(f"Bank ${bank}   Bet ${bet}  [+/-]", True, (255, 230, 200)), (620, 28))

        pygame.draw.ellipse(screen, (20, 90, 50), (40, 120, 880, 360))
        pygame.draw.ellipse(screen, (255, 200, 80), (40, 120, 880, 360), 4)

        if player:
            for i, card in enumerate(player):
                r = draw_card(screen, font, big, card, 80 + i * 160, 240, held[i] if phase == "hold" else False)
                if phase == "hold":
                    tag = "HOLD" if held[i] else "swap"
                    screen.blit(small.render(tag, True, (255, 230, 120) if held[i] else (200, 200, 210)), (r.x + 30, r.bottom + 8))
            if last and phase == "result":
                screen.blit(font.render(last, True, (255, 230, 120)), (400, 180))
        else:
            screen.blit(font.render("Press DEAL to start", True, (230, 230, 240)), (370, 280))

        screen.blit(font.render(msg, True, (255, 240, 220)), (40, 500))
        label = "DEAL" if phase != "hold" else "DRAW"
        pygame.draw.rect(screen, (180, 40, 80), (360, 520, 240, 52), border_radius=12)
        screen.blit(font.render(label + "  (D)", True, (255, 255, 255)), (430, 534))
        screen.blit(small.render("Pair+ pays  ·  Esc quit", True, (180, 150, 170)), (40, 90))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
