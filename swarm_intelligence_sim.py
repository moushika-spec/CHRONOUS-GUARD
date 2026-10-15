# type:ignore 
import pygame
import sys
import math
import random

# ==========================================
# 1. INDUSTRIAL GREY PALETTE & SYSTEM CONFIG
# ==========================================
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Background & Container Panels (Updated to Grey Theme)
COLOR_BG = (32, 36, 44)               # Sleek Industrial Grey Background
COLOR_GRID = (50, 56, 68)             # Grid Alignment Lines
COLOR_PANEL = (22, 26, 33)            # Panel Surface Background
COLOR_PANEL_BORDER = (65, 75, 95)     # Card Edge Border

# Rich Accent Tones
COLOR_DARK_BLUE = (30, 100, 220)      # Core System / Edge Node Indigo
COLOR_DARK_GREEN = (20, 160, 90)      # Nominal / Baseline Health Metric
COLOR_DARK_YELLOW = (210, 150, 10)    # Fault Warnings / Physical Obstacles
COLOR_DARK_RED = (180, 30, 40)        # Anomaly Detection / Hazard Vectors
COLOR_DARK_CYAN = (0, 140, 170)       # Sensor Stream Raycasting

# High Contrast Typography
COLOR_TEXT_BRIGHT = (255, 255, 255)   # White Header Text
COLOR_TEXT_MUTED = (175, 185, 205)    # Readable Slate Labels

# ==========================================
# 2. AUTONOMOUS BOT AGENT (LiDAR + FLOCKING)
# ==========================================
class SwarmAgent:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.acc = pygame.math.Vector2(0, 0)
        self.max_speed = 3.8
        self.max_force = 0.20
        self.radius = 9
        self.lidar_rays = 8
        self.lidar_range = 80
        self.lidar_distances = [self.lidar_range] * self.lidar_rays

    def update(self):
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel
        self.acc *= 0  # Reset steering acceleration

    def apply_force(self, force):
        self.acc += force

    def seek(self, target_pos):
        desired = (target_pos - self.pos)
        dist = desired.length()
        if dist > 0:
            desired = desired.normalize() * self.max_speed
            steer = desired - self.vel
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer
        return pygame.math.Vector2(0, 0)

    def avoid_obstacles(self, obstacles):
        steer = pygame.math.Vector2(0, 0)
        for idx in range(self.lidar_rays):
            angle = (2 * math.pi / self.lidar_rays) * idx
            ray_dir = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            closest_hit = self.lidar_range

            for obs_pos, obs_r in obstacles:
                to_obs = obs_pos - self.pos
                proj = to_obs.dot(ray_dir)
                if proj > 0:
                    perp_dist = math.sqrt(max(0, to_obs.length_squared() - proj**2))
                    if perp_dist < obs_r + self.radius and proj < closest_hit:
                        closest_hit = proj

            self.lidar_distances[idx] = closest_hit

            # Apply strong repulsion force if obstacle detected within range
            if closest_hit < self.lidar_range:
                repel_mag = (self.lidar_range - closest_hit) / self.lidar_range
                steer -= ray_dir * repel_mag * 1.8

        if steer.length() > self.max_force * 2.5:
            steer.scale_to_length(self.max_force * 2.5)
        return steer

    def flock(self, agents):
        alignment = pygame.math.Vector2(0, 0)
        cohesion = pygame.math.Vector2(0, 0)
        separation = pygame.math.Vector2(0, 0)
        total = 0

        for other in agents:
            if other is self:
                continue
            d = self.pos.distance_to(other.pos)
            if 0 < d < 65:
                alignment += other.vel
                cohesion += other.pos
                if d < 28:
                    diff = (self.pos - other.pos).normalize() / d
                    separation += diff
                total += 1

        if total > 0:
            alignment = (alignment / total).normalize() * self.max_speed - self.vel
            cohesion = (cohesion / total - self.pos).normalize() * self.max_speed - self.vel
            separation = separation * 2.2

        return alignment * 0.4 + cohesion * 0.3 + separation * 1.2

# ==========================================
# 3. DRAWING & TYPOGRAPHY HELPERS
# ==========================================
def draw_card(surface, rect, border_color=COLOR_PANEL_BORDER, fill_color=COLOR_PANEL, radius=12):
    pygame.draw.rect(surface, fill_color, rect, border_radius=radius)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=radius)

def draw_grid(surface):
    for x in range(0, 840, 40):
        pygame.draw.line(surface, COLOR_GRID, (x + 400, 20), (x + 400, 660), 1)
    for y in range(0, 640, 40):
        pygame.draw.line(surface, COLOR_GRID, (400, y + 20), (1240, y + 20), 1)

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
    pygame.display.set_caption("CHRONOS-GUARD: Predictive Maintenance Digital Twin Engine")
    clock = pygame.time.Clock()

    # Typography Settings
    font_title = pygame.font.SysFont("Verdana", 21, bold=True)
    font_header = pygame.font.SysFont("Verdana", 17, bold=True)
    font_body = pygame.font.SysFont("Segoe UI", 15, bold=True)
    font_small = pygame.font.SysFont("Segoe UI", 13, bold=True)

    # Simulation Entities
    agents = [SwarmAgent(random.randint(480, 750), random.randint(200, 500)) for _ in range(16)]
    target = pygame.math.Vector2(1040, 340)
    target_vel = pygame.math.Vector2(0, 2.2)
    obstacles = [
        (pygame.math.Vector2(640, 340), 48),
        (pygame.math.Vector2(860, 200), 38),
        (pygame.math.Vector2(860, 480), 38)
    ]

    # Metrics sliding window
    cohesion_history = [50.0] * 60

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(COLOR_BG)

        # Process Mouse & Keyboard Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Check click inside view region
                if 400 <= mx <= 1240 and 20 <= my <= 660:
                    if event.button == 1:    # Left Click: Inject Mechanical Fault / Defect Zone
                        obstacles.append((pygame.math.Vector2(mx, my), random.randint(30, 45)))
                        if len(obstacles) > 6:
                            obstacles.pop(0)
                    elif event.button == 3:  # Right Click: Relocate Optimal Operating Target
                        target = pygame.math.Vector2(mx, my)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset Sensor Telemetry & Node State
                    agents = [SwarmAgent(random.randint(480, 750), random.randint(200, 500)) for _ in range(16)]
                    obstacles = [(pygame.math.Vector2(640, 340), 48)]

        # Move Beacon Target Automatically
        target += target_vel
        if target.y < 60 or target.y > 620:
            target_vel.y *= -1

        # Calculate Physics & Sensor Trajectories
        avg_speed = 0
        total_dist_to_target = 0
        for agent in agents:
            seek_force = agent.seek(target)
            avoid_force = agent.avoid_obstacles(obstacles)
            flock_force = agent.flock(agents)

            agent.apply_force(seek_force * 1.0)
            agent.apply_force(avoid_force * 2.4)
            agent.apply_force(flock_force * 0.8)

            agent.update()
            avg_speed += agent.vel.length()
            total_dist_to_target += agent.pos.distance_to(target)

        avg_speed /= len(agents)
        cohesion_val = max(10, min(100, 100 - (total_dist_to_target / len(agents)) * 0.15))
        cohesion_history.pop(0)
        cohesion_history.append(cohesion_val)

        # ----------------------------------------------------
        # RENDER VIEWPORT (RIGHT SIDE: DIGITAL TWIN WORLD)
        # ----------------------------------------------------
        draw_card(screen, (400, 20, 855, 640), border_color=COLOR_PANEL_BORDER, fill_color=COLOR_PANEL)
        draw_grid(screen)

        # Render Mechanical Defect / Obstacle Zones (Dark Yellow)
        for obs_pos, obs_r in obstacles:
            pygame.draw.circle(screen, (45, 35, 10), obs_pos, obs_r)              # Fault Zone Core
            pygame.draw.circle(screen, COLOR_DARK_YELLOW, obs_pos, obs_r, width=3) # Outer Race Defect Rim
            pygame.draw.circle(screen, COLOR_DARK_YELLOW, obs_pos, 5)

        # Render Optimal Bearing Operating Baseline (Dark Green)
        pygame.draw.circle(screen, COLOR_DARK_GREEN, target, 18, width=3)
        pygame.draw.circle(screen, COLOR_DARK_GREEN, target, 7)
        render_text(screen, "OPTIMAL BASELINE TARGET", font_small, COLOR_DARK_GREEN, (target.x, target.y - 32), center=True)

        # Render Sensor Nodes & Raycast Scanning Beams
        for agent in agents:
            # Draw Raycast Beams
            for i, d in enumerate(agent.lidar_distances):
                angle = (2 * math.pi / agent.lidar_rays) * i
                ray_end = agent.pos + pygame.math.Vector2(math.cos(angle), math.sin(angle)) * d
                beam_color = COLOR_DARK_RED if d < agent.lidar_range * 0.45 else COLOR_DARK_CYAN
                pygame.draw.line(screen, beam_color, agent.pos, ray_end, 2)

            # Draw Edge Telemetry Node (Dark Blue)
            heading_angle = math.atan2(agent.vel.y, agent.vel.x)
            p1 = agent.pos + pygame.math.Vector2(math.cos(heading_angle), math.sin(heading_angle)) * 14
            p2 = agent.pos + pygame.math.Vector2(math.cos(heading_angle + 2.5), math.sin(heading_angle + 2.5)) * 9
            p3 = agent.pos + pygame.math.Vector2(math.cos(heading_angle - 2.5), math.sin(heading_angle - 2.5)) * 9

            pygame.draw.polygon(screen, COLOR_DARK_BLUE, [p1, p2, p3])
            pygame.draw.polygon(screen, COLOR_TEXT_BRIGHT, [p1, p2, p3], width=1)
            pygame.draw.circle(screen, COLOR_TEXT_BRIGHT, agent.pos, 3)

        # ----------------------------------------------------
        # RENDER CONTROL HUD PANEL (LEFT SIDE - CHRONOS-GUARD)
        # ----------------------------------------------------
        draw_card(screen, (20, 20, 360, 640), border_color=COLOR_PANEL_BORDER)

        render_text(screen, "CHRONOS-GUARD CORE", font_title, COLOR_DARK_BLUE, (35, 38))
        render_text(screen, "NASA IMS Telemetry & Digital Twin", font_small, COLOR_TEXT_MUTED, (35, 72))

        # Metric 1: Active Sensor Nodes
        draw_card(screen, (35, 105, 330, 72), border_color=COLOR_PANEL_BORDER)
        render_text(screen, "ACTIVE EDGE SENSOR NODES", font_small, COLOR_TEXT_MUTED, (50, 115))
        render_text(screen, f"{len(agents)} CHANNELS", font_header, COLOR_TEXT_BRIGHT, (50, 140))

        # Metric 2: Mechanical Vibration RMS
        draw_card(screen, (35, 190, 330, 72), border_color=COLOR_PANEL_BORDER)
        render_text(screen, "VIBRATION RMS STRESS", font_small, COLOR_TEXT_MUTED, (50, 200))
        render_text(screen, f"{avg_speed * 0.08:.3f} g", font_header, COLOR_DARK_BLUE, (50, 225))

        # Metric 3: Health Index % & Anomaly Drift Graph
        draw_card(screen, (35, 275, 330, 185), border_color=COLOR_PANEL_BORDER)
        render_text(screen, "EQUIPMENT HEALTH INDEX", font_small, COLOR_TEXT_MUTED, (50, 285))
        render_text(screen, f"{cohesion_val:.1f}%", font_title, COLOR_DARK_GREEN, (50, 310))

        graph_rect = (50, 365, 300, 80)
        draw_card(screen, graph_rect, border_color=COLOR_PANEL_BORDER, fill_color=COLOR_BG)
        pts = []
        for idx, val in enumerate(cohesion_history):
            gx = graph_rect[0] + idx * (graph_rect[2] / len(cohesion_history))
            gy = graph_rect[1] + graph_rect[3] - (val / 100.0) * graph_rect[3]
            pts.append((gx, gy))
        if len(pts) > 1:
            pygame.draw.lines(screen, COLOR_DARK_GREEN, False, pts, 3)

        # Metric 4: Interactive Diagnostic Controls
        draw_card(screen, (35, 470, 330, 175), border_color=COLOR_PANEL_BORDER, fill_color=COLOR_BG)
        render_text(screen, "DIAGNOSTIC CONTROLS", font_header, COLOR_TEXT_BRIGHT, (50, 482))
        controls = [
            "[LEFT CLICK]  Inject Fault / Defect",
            "[RIGHT CLICK] Relocate Baseline Target",
            "[KEY 'R']     Reset System State",
            "Sensor Array: 8 Channels / Node",
            "Scan Bounds:  80 px Proximity"
        ]
        for i, c in enumerate(controls):
            render_text(screen, c, font_body, COLOR_TEXT_MUTED, (50, 515 + i * 24))

        # Bottom System Nav Status Bar
        pygame.draw.rect(screen, COLOR_PANEL, (0, HEIGHT - 40, WIDTH, 40))
        pygame.draw.line(screen, COLOR_PANEL_BORDER, (0, HEIGHT - 40), (WIDTH, HEIGHT - 40), 1)
        render_text(screen, "SYSTEM STATUS: CHRONOS-GUARD INDUSTRIAL GREY TWIN ACTIVE | 60 FPS", font_small, COLOR_TEXT_MUTED, (25, HEIGHT - 26))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()