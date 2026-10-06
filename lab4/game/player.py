import pygame

SPEED = 4

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_y = 0
        self.on_ground = False
        self.color = (60,160,220)

    def update(self, keys, platforms, width):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -13
            self.on_ground = False

        self.vel_y = min(self.vel_y + 0.55, 12)
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x + dx))
        prev_bottom = self.rect.bottom
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if getattr(p, 'is_broken', False):
                continue
            plat_rect = getattr(p, 'rect', p)
            if self.vel_y >= 0:
                is_touching = self.rect.colliderect(plat_rect) or (
                    self.rect.bottom == plat_rect.top and self.rect.right > plat_rect.left and self.rect.left < plat_rect.right
                )
                if is_touching and prev_bottom <= plat_rect.top + 4:
                    self.rect.bottom = plat_rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    if hasattr(p, 'on_player_land'):
                        p.on_player_land(self)
                    break

    def draw(self, screen, cam_y):
        dr = self.rect.move(0, -int(cam_y))
        pygame.draw.rect(screen, self.color, dr, border_radius=6)
        pygame.draw.circle(screen,(255,220,180),(dr.centerx, dr.top+8),7)
