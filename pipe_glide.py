#!/usr/bin/env python3
"""Pipe Glide — colourful flyer through neon pipes. Original, not a clone of any ROM."""
from __future__ import annotations

import random
import sys

import pygame

W, H = 480, 720
GRAVITY = 0.45
FLAP = -7.8
GAP = 190
PIPE_W = 72
SPEED = 3.2


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe Glide")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    big = pygame.font.SysFont("arial", 42, bold=True)

    bird = pygame.Rect(90, H // 2, 34, 28)
    vel = 0.0
    pipes: list[tuple[pygame.Rect, pygame.Rect, bool]] = []
    spawn = 0
    score = 0
    alive = True
    started = False

    def add_pipe() -> None:
        top_h = random.randint(80, H - GAP - 140)
        top = pygame.Rect(W + 10, 0, PIPE_W, top_h)
        bot = pygame.Rect(W + 10, top_h + GAP, PIPE_W, H - (top_h + GAP))
        pipes.append((top, bot, False))

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if not alive:
                        bird.y = H // 2
                        vel = 0
                        pipes.clear()
                        spawn = 0
                        score = 0
                        alive = True
                        started = True
                    else:
                        started = True
                        vel = FLAP
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))

        if started and alive:
            vel += GRAVITY
            bird.y += int(vel)
            spawn += 1
            if spawn >= 90:
                spawn = 0
                add_pipe()
            for i, (top, bot, passed) in enumerate(list(pipes)):
                top.x -= int(SPEED)
                bot.x -= int(SPEED)
                if not passed and top.right < bird.left:
                    pipes[i] = (top, bot, True)
                    score += 1
            pipes[:] = [(t, b, p) for t, b, p in pipes if t.right > -10]
            if bird.top < 0 or bird.bottom > H - 50:
                alive = False
            for top, bot, _ in pipes:
                if bird.colliderect(top) or bird.colliderect(bot):
                    alive = False

        screen.fill((40, 170, 230))
        for i in range(6):
            pygame.draw.circle(screen, (255, 255, 255), (60 + i * 80, 80 + (i % 3) * 30), 18 + i % 3 * 6)
        pygame.draw.rect(screen, (50, 180, 80), (0, H - 50, W, 50))
        pygame.draw.rect(screen, (40, 140, 60), (0, H - 50, W, 8))

        for top, bot, _ in pipes:
            pygame.draw.rect(screen, (60, 200, 80), top)
            pygame.draw.rect(screen, (40, 140, 50), top, 3)
            pygame.draw.rect(screen, (60, 200, 80), bot)
            pygame.draw.rect(screen, (40, 140, 50), bot, 3)
            cap = pygame.Rect(top.x - 6, top.bottom - 18, PIPE_W + 12, 18)
            cap2 = pygame.Rect(bot.x - 6, bot.top, PIPE_W + 12, 18)
            pygame.draw.rect(screen, (80, 230, 100), cap)
            pygame.draw.rect(screen, (80, 230, 100), cap2)

        body = (255, 220, 50) if alive else (180, 80, 80)
        pygame.draw.ellipse(screen, body, bird)
        pygame.draw.circle(screen, (20, 20, 20), (bird.centerx + 8, bird.centery - 4), 4)
        pygame.draw.polygon(
            screen,
            (255, 120, 40),
            [(bird.right - 2, bird.centery), (bird.right + 12, bird.centery - 5), (bird.right + 12, bird.centery + 5)],
        )

        screen.blit(big.render(str(score), True, (20, 40, 60)), (W // 2 - 12, 20))
        if not started:
            screen.blit(font.render("SPACE to glide", True, (20, 40, 60)), (150, H // 2 - 80))
        if not alive:
            screen.blit(font.render("Crashed — SPACE to retry", True, (20, 40, 60)), (110, H // 2 + 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
