#!/usr/bin/env python3
"""Space Raiders — colourful invader-style shooter (original)."""

import random
import sys

import pygame

WIDTH, HEIGHT = 900, 640


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Raiders — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    big = pygame.font.SysFont("arial", 48, bold=True)

    player = pygame.Rect(WIDTH // 2 - 18, HEIGHT - 70, 36, 22)
    bullets: list[pygame.Rect] = []
    enemies: list[list] = []
    for row in range(5):
        for col in range(9):
            enemies.append([80 + col * 80, 70 + row * 48, 1, row])
    edir = 1
    score = 0
    lives = 3
    cooldown = 0
    bombs: list[pygame.Rect] = []
    over = False
    win = False

    while True:
        shoot = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_r and (over or win):
                    return main()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 7
        player.x = max(10, min(WIDTH - 46, player.x))

        if not over and not win:
            cooldown = max(0, cooldown - 1)
            if shoot and cooldown == 0:
                bullets.append(pygame.Rect(player.centerx - 3, player.y - 12, 6, 14))
                cooldown = 12

            for b in bullets:
                b.y -= 10
            bullets = [b for b in bullets if b.y > -20]

            edge = False
            for e in enemies:
                e[0] += edir * (1.4 + score / 800)
                if e[0] < 20 or e[0] > WIDTH - 50:
                    edge = True
            if edge:
                edir *= -1
                for e in enemies:
                    e[1] += 16

            if enemies and random.random() < 0.03:
                shooter = random.choice(enemies)
                bombs.append(pygame.Rect(int(shooter[0]) + 14, int(shooter[1]) + 28, 6, 12))
            for bomb in bombs:
                bomb.y += 5
            bombs = [b for b in bombs if b.y < HEIGHT + 20]

            still = []
            for e in enemies:
                er = pygame.Rect(int(e[0]), int(e[1]), 36, 26)
                hit = False
                for b in bullets[:]:
                    if b.colliderect(er):
                        bullets.remove(b)
                        score += 50 + e[3] * 10
                        hit = True
                        break
                if not hit:
                    still.append(e)
                    if er.bottom >= player.y:
                        over = True
            enemies = still
            if not enemies:
                win = True

            for bomb in bombs[:]:
                if bomb.colliderect(player):
                    bombs.remove(bomb)
                    lives -= 1
                    if lives <= 0:
                        over = True

        screen.fill((8, 10, 28))
        for i in range(40):
            pygame.draw.circle(screen, (180, 200, 255), ((i * 97) % WIDTH, (i * 53) % 400), 1)

        pygame.draw.polygon(
            screen,
            (80, 220, 255),
            [
                (player.centerx, player.y - 8),
                (player.left, player.bottom),
                (player.right, player.bottom),
            ],
        )
        pygame.draw.rect(screen, (40, 140, 220), player, border_radius=3)

        palette = [(255, 90, 160), (255, 180, 60), (90, 255, 140), (120, 160, 255), (220, 110, 255)]
        for e in enemies:
            color = palette[e[3] % len(palette)]
            body = pygame.Rect(int(e[0]), int(e[1]), 36, 26)
            pygame.draw.rect(screen, color, body, border_radius=6)
            pygame.draw.rect(screen, (20, 20, 40), (body.x + 6, body.y + 8, 8, 8))
            pygame.draw.rect(screen, (20, 20, 40), (body.x + 22, body.y + 8, 8, 8))

        for b in bullets:
            pygame.draw.rect(screen, (255, 240, 80), b, border_radius=2)
        for bomb in bombs:
            pygame.draw.rect(screen, (255, 80, 80), bomb, border_radius=2)

        screen.blit(font.render(f"SCORE  {score}", True, (255, 230, 120)), (16, 10))
        screen.blit(font.render(f"LIVES  {lives}", True, (255, 120, 140)), (16, 36))
        screen.blit(font.render("x.com/ElbowOS", True, (160, 180, 220)), (WIDTH - 200, 12))

        if over:
            msg = big.render("GAME OVER", True, (255, 70, 90))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            screen.blit(font.render("Press R to restart", True, (240, 240, 255)), (WIDTH // 2 - 90, HEIGHT // 2 + 40))
        elif win:
            msg = big.render("SECTOR CLEAR", True, (90, 255, 160))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            screen.blit(font.render("Press R to play again", True, (240, 240, 255)), (WIDTH // 2 - 100, HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
