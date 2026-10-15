# CHRONOS-GUARD | Acoustic Emission & PZT Triangulation NDE (Optimized Typography)
import math
import random
import sys
import pygame

# ==========================================
# 1. INDUSTRIAL GREY PALETTE & SYSTEM CONFIG
# ==========================================
WIDTH, HEIGHT = 1280, 720
FPS = 60

COLOR_BG = (70, 76, 88)
COLOR_GRID = (50, 56, 68)
COLOR_PANEL = (32, 38, 50)
COLOR_PANEL_BORDER = (110, 125, 150)
COLOR_PLOT_BG = (20, 24, 34)

ACCENT_BLUE = (56, 189, 248)
ACCENT_GREEN = (74, 222, 128)
ACCENT_AMBER = (251, 191, 36)
ACCENT_RED = (248, 113, 113)
ACCENT_PURPLE = (192, 132, 252)

COLOR_TEXT_BRIGHT = (255, 255, 255)
COLOR_TEXT_MUTED = (205, 215, 235)  # Brighter & Larger Muted Grey Text

# ==========================================
# 2. ADVANCED ACOUSTIC & PARTICLE CLASSES
# ==========================================
class AcousticImpact:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 4.0
        self.max_radius = 360.0
        self.speed = 4.2
        self.intensity = 1.0
        self.alive = True
        self.particles = []
        for _ in range(16):
            ang = random.uniform(0, 2 * math.pi)
            spd = random.uniform(1.5, 4.0)
            self.particles.append({"x": x, "y": y, "vx": math.cos(ang)*spd, "vy": math.sin(ang)*spd, "life": 1.0})

    def update(self):
        self.radius += self.speed
        self.intensity = max(0.0, 1.0 - (self.radius / self.max_radius))
        if self.radius >= self.max_radius:
            self.alive = False
        
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 0.025

# ==========================================
# 3. DRAWING & HELPERS
# ==========================================
def draw_card(surface, rect, border_color=COLOR_PANEL_BORDER, fill_color=COLOR_PANEL, radius=8):
    rx, ry, rw, rh = rect
    shadow = pygame.Rect(rx + 2, ry + 3, rw, rh)
    pygame.draw.rect(surface, (45, 50, 60), shadow, border_radius=radius)
    pygame.draw.rect(surface, fill_color, rect, border_radius=radius)
    pygame.draw.rect(surface, border_color, rect, width=1, border_radius=radius)

def render_text(surface, text, font, color, pos, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(img, rect)

# ==========================================
# 4. MAIN APPLICATION ENGINE
# ==========================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CHRONOS-GUARD: PZT Triangulation & Acoustic Emission")
    clock = pygame.time.Clock()

    # Upgraded font sizes for grey labels and subheadings
    font_title = pygame.font.SysFont("Segoe UI", 18, bold=True)
    font_header = pygame.font.SysFont("Segoe UI", 16, bold=True)
    font_body = pygame.font.SysFont("Segoe UI", 15)       # Increased from 14
    font_small = pygame.font.SysFont("Consolas", 14, bold=True) # Increased from 13

    max_points = 120
    ae_waveform = [0.0] * max_points
    db_history = [45.0] * max_points
    impacts = []

    pzt_sensors = [
        (460, 80, "PZT-A"),
        (1180, 80, "PZT-B"),
        (460, 600, "PZT-C"),
        (1180, 600, "PZT-D")
    ]

    impacts.append(AcousticImpact(820, 340))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        screen.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 420 <= mx <= 1220 and 40 <= my <= 640:
                    if event.button == 1:
                        impacts.append(AcousticImpact(mx, my))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    impacts.clear()
                    ae_waveform = [0.0] * max_points

        for imp in impacts[:]:
            imp.update()
            if not imp.alive:
                impacts.remove(imp)

        if random.random() < 0.025 and len(impacts) < 3:
            impacts.append(AcousticImpact(random.randint(520, 1120), random.randint(120, 540)))

        active_intensity = sum([i.intensity for i in impacts])
        noise = random.gauss(0, 0.12)
        signal_val = (active_intensity * 4.2) + noise
        ae_waveform.append(signal_val)
        ae_waveform.pop(0)

        current_db = 45.0 + (active_intensity * 42.0) + random.uniform(-1.0, 1.0)
        db_history.append(current_db)
        db_history.pop(0)

        # ----------------------------------------------------
        # VIEWPORT: DYNAMIC PZT MESH & STRESS SHOCKWAVES
        # ----------------------------------------------------
        draw_card(screen, (400, 20, 840, 640))
        
        for x in range(440, 1200, 80):
            pygame.draw.line(screen, COLOR_GRID, (x, 40), (x, 640), 1)
        for y in range(60, 620, 80):
            pygame.draw.line(screen, COLOR_GRID, (420, y), (1220, y), 1)

        render_text(screen, "HIGH-FIDELITY ULTRASONIC STRESS PROPAGATION & SENSOR MESH", font_small, COLOR_TEXT_MUTED, (420, 32))

        for imp in impacts:
            r = int(imp.radius)
            pygame.draw.circle(screen, ACCENT_BLUE, (imp.x, imp.y), r, width=3)
            if r > 45:
                pygame.draw.circle(screen, ACCENT_PURPLE, (imp.x, imp.y), r - 45, width=2)
            if r > 90:
                pygame.draw.circle(screen, ACCENT_AMBER, (imp.x, imp.y), r - 90, width=1)

            for p in imp.particles:
                if p["life"] > 0:
                    px, py = int(p["x"]), int(p["y"])
                    pygame.draw.circle(screen, ACCENT_RED, (px, py), 2)

            pygame.draw.circle(screen, ACCENT_RED, (imp.x, imp.y), 7)
            pygame.draw.circle(screen, COLOR_TEXT_BRIGHT, (imp.x, imp.y), 3)

            for sx, sy, sname in pzt_sensors:
                dist = math.hypot(imp.x - sx, imp.y - sy)
                if abs(imp.radius - dist) < 10:
                    pygame.draw.line(screen, ACCENT_GREEN, (imp.x, imp.y), (sx, sy), 2)
                elif imp.radius > dist:
                    pygame.draw.line(screen, (70, 110, 90), (imp.x, imp.y), (sx, sy), 1)

        for sx, sy, sname in pzt_sensors:
            triggered = any(abs(imp.radius - math.hypot(imp.x - sx, imp.y - sy)) < 15 for imp in impacts)
            node_color = ACCENT_GREEN if triggered else COLOR_PLOT_BG
            border_col = COLOR_TEXT_BRIGHT if triggered else ACCENT_GREEN

            pygame.draw.circle(screen, node_color, (sx, sy), 14)
            pygame.draw.circle(screen, border_col, (sx, sy), 14, width=3)
            render_text(screen, sname, font_small, COLOR_TEXT_BRIGHT, (sx - 18, sy - 28))

        # ----------------------------------------------------
        # CONTROL HUD PANEL (LEFT SIDE)
        # ----------------------------------------------------
        draw_card(screen, (20, 20, 360, 640))

        render_text(screen, "CHRONOS-GUARD: NDE Core", font_title, ACCENT_BLUE, (35, 38))
        render_text(screen, "PZT Triangulation & Emission Map", font_body, COLOR_TEXT_MUTED, (35, 66))

        # Metric 1
        draw_card(screen, (35, 105, 330, 72))
        render_text(screen, "PEAK ACOUSTIC INTENSITY", font_small, COLOR_TEXT_MUTED, (50, 115))
        render_text(screen, f"{current_db:.1f} dB", font_header, ACCENT_RED if current_db > 65 else ACCENT_BLUE, (50, 140))

        # Metric 2
        draw_card(screen, (35, 190, 330, 72))
        render_text(screen, "ACTIVE STRESS WAVEFRONTS", font_small, COLOR_TEXT_MUTED, (50, 200))
        render_text(screen, f"{len(impacts)} IMPACT EPICENTERS", font_header, ACCENT_GREEN, (50, 225))

        # Metric 3
        draw_card(screen, (35, 275, 330, 185))
        render_text(screen, "AE TIME-DOMAIN ENVELOPE", font_small, COLOR_TEXT_MUTED, (50, 285))
        render_text(screen, f"{signal_val:.3f} mV", font_title, ACCENT_PURPLE, (50, 310))

        graph_rect = (50, 365, 300, 80)
        draw_card(screen, graph_rect, fill_color=COLOR_PLOT_BG)
        pts = []
        for idx, val in enumerate(ae_waveform):
            gx = graph_rect[0] + idx * (graph_rect[2] / len(ae_waveform))
            norm_v = max(0.0, min(1.0, (val + 3.0) / 6.0))
            gy = graph_rect[1] + graph_rect[3] - (norm_v * graph_rect[3])
            pts.append((gx, gy))
        if len(pts) > 1:
            pygame.draw.lines(screen, ACCENT_PURPLE, False, pts, 2)

        # Controls
        draw_card(screen, (35, 470, 330, 155), fill_color=COLOR_PLOT_BG)
        render_text(screen, "NDE INSPECTION CONTROLS", font_header, COLOR_TEXT_BRIGHT, (50, 482))
        controls = [
            "[LEFT CLICK]  Trigger Impact Epicenter",
            "[KEY 'R']     Clear Active Wavefronts",
            "Sensor Array: 4-Channel PZT Grid",
            "Localization: Time-of-Flight ToF"
        ]
        for i, c in enumerate(controls):
            render_text(screen, c, font_body, COLOR_TEXT_MUTED, (50, 518 + i * 24))

        # Footer
        pygame.draw.rect(screen, COLOR_PANEL, (0, HEIGHT - 35, WIDTH, 35))
        pygame.draw.line(screen, COLOR_PANEL_BORDER, (0, HEIGHT - 35), (WIDTH, HEIGHT - 35), 1)
        render_text(screen, "SYSTEM STATUS: PZT TRIANGULATION ACTIVE | 60 FPS", font_small, COLOR_TEXT_MUTED, (25, HEIGHT - 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()