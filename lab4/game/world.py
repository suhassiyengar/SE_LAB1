import pygame
import random

PLATFORM_COLOR = (100,80,50)
CRUMBLE_COLOR = (180,95,50)
SPRING_COLOR = (45,210,130)
LAVA_COLOR = (220,60,20)

class Platform(pygame.Rect):
    def __init__(self, x, y, width, height, kind="normal"):
        super().__init__(x, y, width, height)
        self.kind = kind  # "normal", "crumbling", "spring"
        
        # Crumble state
        self.stepped_on = False
        self.crumble_timer = 50
        self.max_crumble_time = 50
        self.is_broken = False
        self.shake_offset_x = 0
        self.debris = []
        
        # Spring state
        self.spring_bounce = 0
        self.spring_particles = []

    def on_player_land(self, player):
        if self.kind == "crumbling" and not self.stepped_on:
            self.stepped_on = True
        elif self.kind == "spring":
            self.trigger_spring(player)

    def trigger_spring(self, player):
        # High-velocity launch upward (standard jump is -13)
        player.vel_y = -20
        player.on_ground = False
        self.spring_bounce = 12
        for _ in range(12):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-4, 1)
            self.spring_particles.append([
                self.centerx + random.randint(-16, 16),
                self.top,
                vx, vy, random.randint(3, 5), 255
            ])

    def update(self):
        if self.kind == "crumbling":
            if self.stepped_on and not self.is_broken:
                self.crumble_timer -= 1
                intensity = 1 if self.crumble_timer > 20 else 3
                self.shake_offset_x = random.randint(-intensity, intensity)
                if self.crumble_timer <= 0:
                    self.is_broken = True
                    self.shake_offset_x = 0
                    for _ in range(14):
                        vx = random.uniform(-2.5, 2.5)
                        vy = random.uniform(-2.5, 0.5)
                        sz = random.randint(3, 6)
                        self.debris.append([
                            self.x + random.randint(0, self.width),
                            self.y + random.randint(0, self.height),
                            vx, vy, sz, 255
                        ])

        for d in self.debris:
            d[0] += d[2]
            d[1] += d[3]
            d[3] += 0.35
            d[5] = max(0, d[5] - 6)
        self.debris = [d for d in self.debris if d[5] > 0]

        if self.spring_bounce > 0:
            self.spring_bounce -= 1

        for sp in self.spring_particles:
            sp[0] += sp[2]
            sp[1] += sp[3]
            sp[3] += 0.2
            sp[5] = max(0, sp[5] - 12)
        self.spring_particles = [sp for sp in self.spring_particles if sp[5] > 0]

    def draw(self, screen, cam_y):
        # Draw crumbling debris
        for d in self.debris:
            sx = int(d[0])
            sy = int(d[1] - cam_y)
            sz = d[4]
            alpha = int(d[5])
            deb_surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
            deb_surf.fill((180, 95, 50, alpha))
            screen.blit(deb_surf, (sx, sy))

        # Draw spring launch particles
        for sp in self.spring_particles:
            sx = int(sp[0])
            sy = int(sp[1] - cam_y)
            sz = sp[4]
            alpha = int(sp[5])
            sp_surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
            sp_surf.fill((60, 255, 160, alpha))
            screen.blit(sp_surf, (sx, sy))

        if self.is_broken:
            return

        dr = self.move(self.shake_offset_x, -int(cam_y))

        if self.kind == "crumbling":
            t_ratio = self.crumble_timer / self.max_crumble_time if self.stepped_on else 1.0
            r = min(255, int(180 + (1 - t_ratio) * 75))
            g = max(35, int(95 * t_ratio))
            b = max(25, int(50 * t_ratio))
            base_col = (r, g, b)
            pygame.draw.rect(screen, base_col, dr, border_radius=4)
            pygame.draw.line(screen, (60, 25, 10), (dr.left + dr.width//3, dr.top), (dr.left + dr.width//3 + 4, dr.bottom - 2), 2)
            pygame.draw.line(screen, (60, 25, 10), (dr.left + 2*dr.width//3, dr.top + 2), (dr.left + 2*dr.width//3 - 5, dr.bottom), 2)
            pygame.draw.line(screen, (225, 145, 95), (dr.left + 2, dr.top), (dr.right - 2, dr.top), 1)

        elif self.kind == "spring":
            # Metallic spring base
            pygame.draw.rect(screen, (40, 70, 60), dr, border_radius=4)
            # Spring coil indicator in center
            compress = 3 if self.spring_bounce > 0 else 0
            pad_rect = pygame.Rect(dr.left + 4, dr.top + compress, dr.width - 8, 5)
            pygame.draw.rect(screen, SPRING_COLOR, pad_rect, border_radius=2)
            # Upward arrows / chevron markings on spring pad
            cx = dr.centerx
            for ox in (-18, 0, 18):
                if dr.left + 10 < cx + ox < dr.right - 10:
                    pts = [(cx + ox - 4, dr.centery + 3), (cx + ox, dr.centery - 2), (cx + ox + 4, dr.centery + 3)]
                    pygame.draw.lines(screen, (120, 255, 190), False, pts, 2)
            pygame.draw.line(screen, (180, 255, 210), (dr.left + 2, dr.top + compress), (dr.right - 2, dr.top + compress), 1)

        else:
            pygame.draw.rect(screen, PLATFORM_COLOR, dr, border_radius=4)
            pygame.draw.line(screen, (140, 115, 80), (dr.left + 2, dr.top), (dr.right - 2, dr.top), 2)

def generate_platforms(width, base_y, count=30):
    plats = [Platform(0, base_y, width, 20, kind="normal")]  # ground
    y = base_y - 110
    prev_kind = "normal"
    for i in range(count):
        w = random.randint(80, 200)
        x = random.randint(0, width - w)
        if i == count - 1:
            kind = "normal"
            w = max(w, 140)
        else:
            roll = random.random()
            if prev_kind != "normal":
                # Ensure spacing between hazards/specials
                kind = "normal" if roll < 0.65 else ("spring" if prev_kind == "crumbling" else "crumbling")
            else:
                if roll < 0.28:
                    kind = "crumbling"
                elif roll < 0.50:
                    kind = "spring"
                else:
                    kind = "normal"
        prev_kind = kind
        plats.append(Platform(x, y, w, 16, kind=kind))
        y -= random.randint(80, 130)
    return plats

def draw_lava(screen, lava_y, cam_y, width, height, frame, surge_active=False, surge_warning=False):
    import math
    ly = int(lava_y - cam_y)
    if ly < height + 40:
        # Dynamic wave amplitude and frequency depending on surge state
        wave_amp = 14 if surge_active else (10 if surge_warning else 8)
        wave_speed = 0.22 if surge_active else (0.15 if surge_warning else 0.10)

        pts = [(0, ly)]
        for x in range(0, width + 20, 20):
            wave = int(math.sin(x * 0.08 + frame * wave_speed) * wave_amp)
            pts.append((x, ly + wave))
        pts.append((width, height + 60))
        pts.append((0, height + 60))

        # Fiery red for surge, default rich lava for normal
        color = (255, 45, 10) if surge_active else LAVA_COLOR
        pygame.draw.polygon(screen, color, pts)

        # Bright crest line
        crest_color = (255, 230, 80) if surge_active else (255, 150, 40)
        pygame.draw.lines(screen, crest_color, False, pts[1:-2], 3 if surge_active else 2)

        # Ambient heat glow
        glow_height = 40 if surge_active else 26
        s = pygame.Surface((width, glow_height), pygame.SRCALPHA)
        glow_color = (255, 50, 0) if surge_active else (255, 100, 0)
        max_alpha = 110 if surge_active else 65
        for i in range(glow_height // 2):
            alpha = max(0, int(max_alpha - i * (max_alpha / (glow_height // 2))))
            pygame.draw.line(s, (*glow_color, alpha), (0, i), (width, i), 1)
        screen.blit(s, (0, ly - (glow_height // 2)))
