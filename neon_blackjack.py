#!/usr/bin/env python3
"""Neon Blackjack — colourful casino card game."""

from __future__ import annotations

import random
import sys

import pygame

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def card_value(rank: str) -> int:
    if rank == "A":
        return 11
    if rank in {"J", "Q", "K"}:
        return 10
    return int(rank)


def hand_total(cards: list[tuple[str, str]]) -> int:
    total = sum(card_value(r) for r, _s in cards)
    aces = sum(1 for r, _s in cards if r == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def new_deck() -> list[tuple[str, str]]:
    deck = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck


def draw_card(surf, x, y, rank, suit, hidden=False):
    rect = pygame.Rect(x, y, 92, 132)
    pygame.draw.rect(surf, (30, 30, 45), rect.inflate(6, 6), border_radius=10)
    if hidden:
        pygame.draw.rect(surf, (80, 30, 120), rect, border_radius=8)
        for i in range(5):
            pygame.draw.rect(surf, (140, 70, 200), (x + 10, y + 14 + i * 22, 72, 12), border_radius=3)
        return
    pygame.draw.rect(surf, (250, 248, 240), rect, border_radius=8)
    red = suit in {"♥", "♦"}
    color = (200, 30, 50) if red else (20, 25, 40)
    font = pygame.font.SysFont("arial", 26, bold=True)
    big = pygame.font.SysFont("arial", 40, bold=True)
    surf.blit(font.render(rank, True, color), (x + 8, y + 6))
    surf.blit(font.render(suit, True, color), (x + 8, y + 32))
    mid = big.render(suit, True, color)
    surf.blit(mid, mid.get_rect(center=(x + 46, y + 80)))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((900, 620))
    pygame.display.set_caption("Neon Blackjack — ElbowOS Arcade")
    clock = pygame.time.Clock()
    title_f = pygame.font.SysFont("arial", 40, bold=True)
    font = pygame.font.SysFont("arial", 24, bold=True)
    small = pygame.font.SysFont("arial", 18)

    bank = 500
    bet = 25
    deck = new_deck()
    player: list[tuple[str, str]] = []
    dealer: list[tuple[str, str]] = []
    phase = "ready"
    message = "Press N for a new hand  ·  H hit  ·  S stand"
    hide_hole = True

    def deal():
        nonlocal deck, player, dealer, phase, message, hide_hole, bank, bet
        if bank < bet:
            message = "Bank empty — game over. Esc to quit."
            phase = "broke"
            return
        if len(deck) < 15:
            deck = new_deck()
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]
        bank -= bet
        hide_hole = True
        phase = "player"
        if hand_total(player) == 21:
            phase = "dealer"
            message = "Blackjack!"
        else:
            message = "H hit   S stand"

    def finish():
        nonlocal phase, message, hide_hole, bank
        hide_hole = False
        phase = "done"
        pt, dt = hand_total(player), hand_total(dealer)
        if pt > 21:
            message = "Bust! Dealer wins."
        elif dt > 21 or pt > dt:
            win = bet * 2
            if pt == 21 and len(player) == 2:
                win = int(bet * 2.5)
            bank += win
            message = f"You win +{win - bet}!"
        elif pt == dt:
            bank += bet
            message = "Push — bet returned."
        else:
            message = "Dealer wins."

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_n and phase in {"ready", "done", "broke"}:
                    if phase != "broke":
                        deal()
                if phase == "player":
                    if event.key == pygame.K_h:
                        player.append(deck.pop())
                        if hand_total(player) >= 21:
                            if hand_total(player) > 21:
                                finish()
                            else:
                                phase = "dealer"
                    if event.key == pygame.K_s:
                        phase = "dealer"

        if phase == "dealer":
            hide_hole = False
            while hand_total(dealer) < 17:
                dealer.append(deck.pop())
            finish()

        screen.fill((8, 70, 42))
        pygame.draw.rect(screen, (6, 50, 30), (40, 30, 820, 560), border_radius=24)
        pygame.draw.rect(screen, (20, 140, 80), (40, 30, 820, 560), 4, border_radius=24)

        screen.blit(title_f.render("NEON BLACKJACK", True, (255, 220, 80)), (60, 48))
        screen.blit(small.render("x.com/ElbowOS", True, (180, 230, 190)), (700, 58))
        screen.blit(font.render(f"Bank  ${bank}    Bet  ${bet}", True, (240, 255, 240)), (60, 100))

        screen.blit(font.render(f"Dealer  {'' if hide_hole else hand_total(dealer)}", True, (230, 240, 255)), (60, 150))
        for i, (r, s) in enumerate(dealer):
            draw_card(screen, 60 + i * 104, 185, r, s, hidden=(hide_hole and i == 0))

        screen.blit(font.render(f"You  {hand_total(player) if player else ''}", True, (255, 240, 180)), (60, 340))
        for i, (r, s) in enumerate(player):
            draw_card(screen, 60 + i * 104, 375, r, s)

        bar = pygame.Rect(60, 530, 780, 40)
        pygame.draw.rect(screen, (10, 40, 28), bar, border_radius=8)
        screen.blit(small.render(message + "   ·   N new hand", True, (255, 255, 210)), (74, 540))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
