import pygame
import random
import math
from game.player import Player
from game.world import generate_platforms, draw_lava, PLATFORM_COLOR

WIDTH,HEIGHT=500,640
FPS=60
BG=(20,15,30)
GROUND_Y=HEIGHT+200

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Lava Escape")
        self.clock=pygame.time.Clock()
        self.small_font=pygame.font.SysFont("monospace",13,bold=True)
        self.font=pygame.font.SysFont("monospace",20,bold=True)
        self.big_font=pygame.font.SysFont("monospace",40,bold=True)
        self.reset()

    def reset(self):
        self.platforms=generate_platforms(WIDTH,GROUND_Y)
        self.player=Player(WIDTH//2-16,GROUND_Y-50)
        self.cam_y=0
        self.lava_y=GROUND_Y+60
        self.lava_rise=0.4
        self.current_lava_speed=0.4
        self.surge_warning=False
        self.surge_active=False
        self.lava_sparks=[]
        self.score=0
        self.game_over=False
        self.won=False
        self.top_y=self.platforms[-1].y
        self.frame=0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        if self.game_over or self.won: return
        keys=pygame.key.get_pressed()
        self.player.update(keys,self.platforms,WIDTH)
        for p in self.platforms:
            if hasattr(p, 'update'):
                p.update()
        target=self.player.rect.centery-HEIGHT//2
        if target<self.cam_y: self.cam_y=target

        # Surge cycle mechanics (cycle of 540 frames ≈ 9s at 60fps)
        surge_cycle = self.frame % 540
        self.surge_warning = (380 <= surge_cycle < 450)
        self.surge_active = (450 <= surge_cycle < 540)

        # Base lava rise increases over time
        self.lava_rise = min(1.2, self.lava_rise + 0.0003)

        if self.surge_active:
            self.current_lava_speed = self.lava_rise * 2.6
            for _ in range(3):
                px = random.randint(0, WIDTH)
                py = self.lava_y
                vx = random.uniform(-1.8, 1.8)
                vy = random.uniform(-7, -2.5)
                self.lava_sparks.append([px, py, vx, vy, random.randint(3, 6), 255])
        else:
            self.current_lava_speed = self.lava_rise

        self.lava_y -= self.current_lava_speed

        # Update lava burst sparks
        for spk in self.lava_sparks:
            spk[0] += spk[2]
            spk[1] += spk[3]
            spk[3] += 0.25
            spk[5] = max(0, spk[5] - 7)
        self.lava_sparks = [spk for spk in self.lava_sparks if spk[5] > 0]

        self.score=max(0,(GROUND_Y-self.player.rect.y)//10)
        self.frame+=1
        if self.player.rect.bottom>=self.lava_y:
            self.game_over=True
        if self.player.rect.top<=self.top_y-20:
            self.won=True

    def _draw_hud(self):
        # 1. Height Score & Hint
        sc = self.font.render(f"Height: {self.score}m", True, (230, 220, 200))
        self.screen.blit(sc, (10, 8))
        hint = self.small_font.render("R=Restart", True, (150, 140, 130))
        self.screen.blit(hint, (10, 30))

        # 2. Rising Danger Meter HUD
        meter_x = WIDTH - 170
        meter_y = 8
        meter_w = 160
        meter_h = 36

        meter_bg = pygame.Surface((meter_w, meter_h), pygame.SRCALPHA)
        meter_bg.fill((15, 12, 22, 210))
        self.screen.blit(meter_bg, (meter_x, meter_y))

        max_speed = 3.2
        ratio = min(1.0, self.current_lava_speed / max_speed)

        if self.surge_active:
            pulse = int((math.sin(self.frame * 0.3) + 1) * 30)
            bar_color = (min(255, 225 + pulse), 30, 30)
            status_text = "SURGE BURST!"
            status_color = (255, 90, 80)
            border_color = (255, 60, 40)
        elif self.surge_warning:
            bar_color = (255, 170, 0) if (self.frame // 10) % 2 == 0 else (210, 120, 0)
            status_text = "SURGE IMMINENT"
            status_color = (255, 200, 50)
            border_color = (240, 160, 30)
        elif ratio < 0.22:
            bar_color = (50, 210, 100)
            status_text = "DANGER: LOW"
            status_color = (130, 230, 150)
            border_color = (50, 70, 60)
        elif ratio < 0.35:
            bar_color = (230, 190, 40)
            status_text = "DANGER: MED"
            status_color = (240, 210, 100)
            border_color = (80, 75, 40)
        else:
            bar_color = (240, 110, 30)
            status_text = "DANGER: HIGH"
            status_color = (255, 140, 70)
            border_color = (100, 55, 30)

        pygame.draw.rect(self.screen, border_color, (meter_x, meter_y, meter_w, meter_h), 1, border_radius=4)

        lbl = self.small_font.render(status_text, True, status_color)
        spd_lbl = self.small_font.render(f"{self.current_lava_speed:.1f}x", True, (210, 200, 190))
        self.screen.blit(lbl, (meter_x + 6, meter_y + 4))
        self.screen.blit(spd_lbl, (meter_x + meter_w - spd_lbl.get_width() - 6, meter_y + 4))

        bar_x = meter_x + 6
        bar_y = meter_y + 21
        bar_max_w = meter_w - 12
        bar_fill_w = max(4, int(bar_max_w * ratio))
        pygame.draw.rect(self.screen, (35, 30, 40), (bar_x, bar_y, bar_max_w, 8), border_radius=3)
        pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, bar_fill_w, 8), border_radius=3)

        # Flashing surge notification banner
        if self.surge_warning and (self.frame // 12) % 2 == 0:
            warn_txt = self.font.render("! LAVA SURGE WARNING !", True, (255, 190, 40))
            self.screen.blit(warn_txt, (WIDTH // 2 - warn_txt.get_width() // 2, 50))
        elif self.surge_active:
            surge_txt = self.font.render(">>> LAVA SURGE ACTIVE! <<<", True, (255, 60, 40))
            self.screen.blit(surge_txt, (WIDTH // 2 - surge_txt.get_width() // 2, 50))

    def draw(self):
        self.screen.fill(BG)
        for p in self.platforms:
            if hasattr(p, 'draw'):
                p.draw(self.screen, self.cam_y)
            else:
                dr=p.move(0,-int(self.cam_y))
                pygame.draw.rect(self.screen,PLATFORM_COLOR,dr,border_radius=4)
        self.player.draw(self.screen,self.cam_y)

        # Draw lava burst sparks
        for spk in self.lava_sparks:
            sx = int(spk[0])
            sy = int(spk[1] - self.cam_y)
            sz = spk[4]
            surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
            surf.fill((255, random.randint(120, 220), 40, int(spk[5])))
            self.screen.blit(surf, (sx, sy))

        draw_lava(self.screen,self.lava_y,self.cam_y,WIDTH,HEIGHT,self.frame,self.surge_active,self.surge_warning)
        self._draw_hud()

        if self.game_over:
            self._msg("LAVA GOT YOU!",(220,80,40))
        if self.won:
            self._msg("ESCAPED!",(80,220,100))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        s=self.font.render("Press R to Play Again",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
        self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2+20))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
