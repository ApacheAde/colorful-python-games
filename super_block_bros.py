#!/usr/bin/env python3
"""Super Block Bros — original colourful platformer (not an emulator)."""

import sys

import pygame

WIDTH, HEIGHT = 960, 540
GRAVITY = 0.55
JUMP = -12.5
SPEED = 5.2


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 40)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP
            self.on_ground = False

        self.vy += GRAVITY
        self.rect.x += int(self.vx)
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vx > 0:
                    self.rect.right = p.left
                elif self.vx < 0:
                    self.rect.left = p.right

        self.rect.y += int(self.vy)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0

    def draw(self, surf, cam):
        r = self.rect.move(-cam, 0)
        body = pygame.Rect(r.x + 4, r.y + 10, 24, 26)
        pygame.draw.rect(surf, (220, 40, 40), body, border_radius=4)
        pygame.draw.rect(surf, (40, 90, 220), (r.x + 6, r.y + 24, 20, 14), border_radius=3)
        pygame.draw.ellipse(surf, (255, 210, 160), (r.x + 6, r.y, 20, 16))
        eye_x = r.x + (14 if self.facing > 0 else 8)
        pygame.draw.circle(surf, (20, 20, 30), (eye_x, r.y + 7), 3)
        pygame.draw.rect(surf, (180, 30, 30), (r.x + 2, r.y - 4, 28, 8), border_radius=3)


class Enemy:
    def __init__(self, x, y, left, right):
        self.rect = pygame.Rect(x, y, 30, 28)
        self.left = left
        self.right = right
        self.dir = 1
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.dir * 2
        if self.rect.x <= self.left or self.rect.x >= self.right:
            self.dir *= -1

    def draw(self, surf, cam):
        if not self.alive:
            return
        r = self.rect.move(-cam, 0)
        pygame.draw.ellipse(surf, (160, 90, 40), r)
        pygame.draw.ellipse(surf, (40, 30, 20), (r.x + 6, r.y + 8, 6, 8))
        pygame.draw.ellipse(surf, (40, 30, 20), (r.x + 18, r.y + 8, 6, 8))


def build_world():
    platforms = [
        pygame.Rect(0, 500, 2800, 50),
        pygame.Rect(220, 410, 140, 22),
        pygame.Rect(430, 340, 120, 22),
        pygame.Rect(620, 280, 160, 22),
        pygame.Rect(860, 380, 110, 22),
        pygame.Rect(1040, 300, 180, 22),
        pygame.Rect(1280, 420, 90, 22),
        pygame.Rect(1420, 340, 150, 22),
        pygame.Rect(1680, 260, 200, 22),
        pygame.Rect(1960, 380, 140, 22),
        pygame.Rect(2180, 300, 220, 22),
        pygame.Rect(2480, 420, 160, 22),
    ]
    coins = [
        pygame.Rect(260, 370, 16, 16),
        pygame.Rect(470, 300, 16, 16),
        pygame.Rect(680, 240, 16, 16),
        pygame.Rect(890, 340, 16, 16),
        pygame.Rect(1100, 260, 16, 16),
        pygame.Rect(1460, 300, 16, 16),
        pygame.Rect(1740, 220, 16, 16),
        pygame.Rect(2000, 340, 16, 16),
        pygame.Rect(2240, 260, 16, 16),
        pygame.Rect(2520, 380, 16, 16),
    ]
    enemies = [
        Enemy(300, 472, 20, 500),
        Enemy(900, 472, 700, 1100),
        Enemy(1500, 472, 1400, 1750),
        Enemy(2100, 472, 2000, 2400),
        Enemy(1100, 272, 1040, 1190),
    ]
    flag = pygame.Rect(2680, 380, 18, 120)
    return platforms, coins, enemies, flag


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Super Block Bros — ElbowOS Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24, bold=True)
    big = pygame.font.SysFont("arial", 48, bold=True)

    platforms, coins, enemies, flag = build_world()
    player = Player(60, 430)
    score = 0
    lives = 3
    cam = 0
    won = False
    dead_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and (lives <= 0 or won):
                platforms, coins, enemies, flag = build_world()
                player = Player(60, 430)
                score = 0
                lives = 3
                cam = 0
                won = False

        if lives > 0 and not won and dead_timer == 0:
            player.update(platforms)
            for e in enemies:
                e.update()
                if e.alive and player.rect.colliderect(e.rect):
                    if player.vy > 0 and player.rect.bottom - e.rect.top < 18:
                        e.alive = False
                        player.vy = JUMP * 0.6
                        score += 200
                    else:
                        lives -= 1
                        dead_timer = 40
                        player = Player(60, 430)
                        cam = 0
            still = []
            for c in coins:
                if player.rect.colliderect(c):
                    score += 100
                else:
                    still.append(c)
            coins = still
            if player.rect.colliderect(flag):
                won = True
            if player.rect.top > HEIGHT + 80:
                lives -= 1
                dead_timer = 40
                player = Player(60, 430)
                cam = 0

        if dead_timer:
            dead_timer -= 1

        cam = max(0, min(player.rect.centerx - WIDTH // 3, 2800 - WIDTH))

        screen.fill((92, 168, 255))
        pygame.draw.rect(screen, (255, 196, 90), (0, 0, WIDTH, 90))
        for cx, cy, r in ((140, 70, 28), (400, 50, 22), (720, 80, 30), (880, 45, 18)):
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), r)
            pygame.draw.circle(screen, (255, 255, 255), (cx + 22, cy + 6), r - 4)

        pygame.draw.ellipse(screen, (60, 170, 90), (-cam * 0.2 - 40, 360, 420, 220))
        pygame.draw.ellipse(screen, (50, 150, 80), (300 - cam * 0.2, 380, 500, 200))

        for p in platforms:
            r = p.move(-cam, 0)
            pygame.draw.rect(screen, (70, 180, 70), r)
            pygame.draw.rect(screen, (120, 80, 40), (r.x, r.bottom - 10, r.w, 10))
            pygame.draw.rect(screen, (40, 120, 40), r, 2)

        for c in coins:
            r = c.move(-cam, 0)
            pygame.draw.ellipse(screen, (255, 210, 40), r)
            pygame.draw.ellipse(screen, (255, 240, 120), r.inflate(-6, -6))

        for e in enemies:
            e.draw(screen, cam)

        fr = flag.move(-cam, 0)
        pygame.draw.rect(screen, (240, 240, 240), (fr.x + 6, fr.y, 6, 120))
        pygame.draw.polygon(screen, (255, 60, 70), [(fr.x + 12, fr.y), (fr.x + 70, fr.y + 22), (fr.x + 12, fr.y + 44)])

        player.draw(screen, cam)

        hud = font.render(f"SCORE  {score}     LIVES  {lives}", True, (20, 30, 50))
        screen.blit(hud, (16, 12))
        brand = font.render("x.com/ElbowOS", True, (20, 40, 80))
        screen.blit(brand, (WIDTH - 200, 12))

        if won:
            msg = big.render("LEVEL CLEAR!", True, (255, 230, 40))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            tip = font.render("Press R to play again", True, (255, 255, 255))
            screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
        elif lives <= 0:
            msg = big.render("GAME OVER", True, (255, 70, 70))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            tip = font.render("Press R to restart", True, (255, 255, 255))
            screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
