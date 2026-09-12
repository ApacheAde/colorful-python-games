#!/usr/bin/env python3
"""Brick Breakout — full-colour arcade brick breaker."""
from __future__ import annotations

import random
import sys

import pygame

W, H = 800, 640
COLS, ROWS = 10, 6
BRICK_W, BRICK_H = 72, 24
GAP = 6
OFFSET_X, OFFSET_Y = 20, 70
PALETTE = [
    (255, 80, 120),
    (255, 140, 60),
    (255, 220, 70),
    (80, 220, 120),
    (70, 180, 255),
    (180, 100, 255),
]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Brick Breakout")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    big = pygame.font.SysFont("arial", 40, bold=True)

    def reset():
        bricks = []
        for r in range(ROWS):
            for c in range(COLS):
                x = OFFSET_X + c * (BRICK_W + GAP)
                y = OFFSET_Y + r * (BRICK_H + GAP)
                bricks.append(pygame.Rect(x, y, BRICK_W, BRICK_H))
        paddle = pygame.Rect(W // 2 - 55, H - 36, 110, 14)
        ball = pygame.Rect(W // 2 - 8, H - 60, 16, 16)
        vel = pygame.Vector2(random.choice([-5, 5]), -5)
        return bricks, paddle, ball, vel, 0, 3, "play"

    bricks, paddle, ball, vel, score, lives, state = reset()

    running = True
    while running:
        dt_frames = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and state != "play":
                    bricks, paddle, ball, vel, score, lives, state = reset()

        keys = pygame.key.get_pressed()
        if state == "play":
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                paddle.x -= 9
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                paddle.x += 9
            paddle.x = max(8, min(W - paddle.w - 8, paddle.x))

            ball.x += int(vel.x)
            ball.y += int(vel.y)
            if ball.left <= 0 or ball.right >= W:
                vel.x *= -1
            if ball.top <= 0:
                vel.y *= -1
            if ball.colliderect(paddle) and vel.y > 0:
                vel.y *= -1
                offset = (ball.centerx - paddle.centerx) / (paddle.w / 2)
                vel.x = max(-8, min(8, vel.x + offset * 3))
            hit = ball.collidelist(bricks)
            if hit != -1:
                bricks.pop(hit)
                vel.y *= -1
                score += 10
                if abs(vel.x) < 9:
                    vel *= 1.03
            if ball.top > H:
                lives -= 1
                ball.center = (paddle.centerx, H - 60)
                vel = pygame.Vector2(random.choice([-5, 5]), -5)
                if lives <= 0:
                    state = "lose"
            if not bricks:
                state = "win"

        screen.fill((10, 12, 28))
        pygame.draw.rect(screen, (24, 18, 48), (0, 0, W, 50))
        screen.blit(font.render(f"BRICK BREAKOUT   Score {score}   Lives {lives}", True, (240, 230, 255)), (16, 14))

        for i, b in enumerate(bricks):
            color = PALETTE[min(i // COLS, len(PALETTE) - 1)]
            pygame.draw.rect(screen, color, b, border_radius=4)
            pygame.draw.rect(screen, (255, 255, 255), b, 1, border_radius=4)

        pygame.draw.rect(screen, (80, 220, 255), paddle, border_radius=8)
        pygame.draw.circle(screen, (255, 240, 120), ball.center, 8)

        if state != "play":
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            text = "CLEAR!" if state == "win" else "GAME OVER"
            screen.blit(big.render(text, True, (255, 90, 160)), (280, 280))
            screen.blit(font.render("Press R to restart  ·  Esc quit", True, (230, 230, 240)), (250, 340))

        pygame.display.flip()
        _ = dt_frames

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
