#!/usr/bin/env python3
"""Neon Pong — two-tone arcade rally vs the CPU."""

import sys

import pygame

WIDTH, HEIGHT = 900, 540


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Pong — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28, bold=True)
    huge = pygame.font.SysFont("arial", 72, bold=True)

    paddle = pygame.Rect(30, HEIGHT // 2 - 50, 14, 100)
    cpu = pygame.Rect(WIDTH - 44, HEIGHT // 2 - 50, 14, 100)
    ball = pygame.Rect(WIDTH // 2 - 8, HEIGHT // 2 - 8, 16, 16)
    vx, vy = 6.0, 4.0
    you = cpu_score = 0
    pause = 30

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            paddle.y -= 8
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            paddle.y += 8
        paddle.y = max(10, min(HEIGHT - 110, paddle.y))

        target = ball.centery - 50
        if cpu.y + 8 < target:
            cpu.y += 6
        elif cpu.y - 8 > target:
            cpu.y -= 6
        cpu.y = max(10, min(HEIGHT - 110, cpu.y))

        if pause:
            pause -= 1
        else:
            ball.x += int(vx)
            ball.y += int(vy)
            if ball.top <= 8 or ball.bottom >= HEIGHT - 8:
                vy *= -1
            if ball.colliderect(paddle) and vx < 0:
                vx = abs(vx) + 0.3
                offset = (ball.centery - paddle.centery) / 50
                vy = offset * 7
            if ball.colliderect(cpu) and vx > 0:
                vx = -(abs(vx) + 0.3)
                offset = (ball.centery - cpu.centery) / 50
                vy = offset * 7
            if ball.right < 0:
                cpu_score += 1
                ball.center = (WIDTH // 2, HEIGHT // 2)
                vx, vy = 6.0, 4.0
                pause = 40
            if ball.left > WIDTH:
                you += 1
                ball.center = (WIDTH // 2, HEIGHT // 2)
                vx, vy = -6.0, -4.0
                pause = 40

        screen.fill((10, 8, 28))
        pygame.draw.rect(screen, (40, 20, 70), (0, 0, WIDTH, HEIGHT), 10)
        for y in range(16, HEIGHT, 28):
            pygame.draw.rect(screen, (80, 60, 140), (WIDTH // 2 - 3, y, 6, 16))

        pygame.draw.rect(screen, (80, 255, 200), paddle, border_radius=6)
        pygame.draw.rect(screen, (255, 90, 180), cpu, border_radius=6)
        pygame.draw.ellipse(screen, (255, 230, 90), ball)

        screen.blit(huge.render(str(you), True, (80, 255, 200)), (WIDTH // 2 - 90, 20))
        screen.blit(huge.render(str(cpu_score), True, (255, 90, 180)), (WIDTH // 2 + 40, 20))
        screen.blit(font.render("YOU", True, (80, 255, 200)), (60, 16))
        screen.blit(font.render("CPU", True, (255, 90, 180)), (WIDTH - 120, 16))
        screen.blit(font.render("x.com/ElbowOS", True, (160, 150, 200)), (WIDTH // 2 - 90, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
