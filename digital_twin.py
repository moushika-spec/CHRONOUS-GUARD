import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHRONOUS-GUARD: Industrial Bearing Digital Twin Platform")
clock = pygame.time.Clock()

# Color Palette
DARK_BG = (14, 17, 23)
PANEL_BG = (22, 27, 34)
TEXT_COLOR = (201, 209, 217)
GREEN = (46, 160, 67)
YELLOW = (210, 153, 34)
RED = (248, 81, 73)
BLUE = (88, 166, 255)
CYAN = (56, 189, 248)

# State Variables
active_view = 1  # 1: Physical Twin, 2: FFT Spectral Analysis, 3: CMMS Dispatcher
angle = 0
health_score = 0.40
rul_cycles = 100
wave_history = [0] * 150
total_roi_saved = 29607500

def draw_bearing_digital_twin(surface, center, health):
    global angle
    cx, cy = center
    radius = 110
    
    # Calculate vibration wobble (eccentricity)
    wobble_x = random.uniform(-1, 1) * (health - 0.35) * 15
    wobble_y = random.uniform(-1, 1) * (health - 0.35) * 15
    center_wobble = (int(cx + wobble_x), int(cy + wobble_y))
    
    # Outer Ring
    pygame.draw.circle(surface, (48, 54, 61), center_wobble, radius, 14)
    
    # Draw Physical Micro-Spall Crack if degraded
    if health >= 0.48:
        crack_color = RED if health >= 0.58 else YELLOW
        pygame.draw.arc(surface, crack_color, (center_wobble[0]-radius, center_wobble[1]-radius, radius*2, radius*2), 0.2, 0.6, 8)
    
    # Inner Ring
    pygame.draw.circle(surface, (110, 118, 129), center_wobble, radius - 42, 10)
    
    # Status Color
    status_color = GREEN if health < 0.48 else (YELLOW if health < 0.58 else RED)
    
    # Rolling Elements
    num_balls = 8
    orbit_radius = radius - 21
    speed = 0.04 + (health - 0.35) * 0.1
    angle += speed
    
    for i in range(num_balls):
        theta = angle + i * (2 * math.pi / num_balls)
        bx = int(center_wobble[0] + orbit_radius * math.cos(theta))
        by = int(center_wobble[1] + orbit_radius * math.sin(theta))
        pygame.draw.circle(surface, status_color, (bx, by), 11)
        pygame.draw.circle(surface, (255, 255, 255), (bx - 2, by - 2), 3)

def main():
    global active_view, health_score, rul_cycles, wave_history, total_roi_saved
    font = pygame.font.SysFont("Segoe UI", 16)
    bold_font = pygame.font.SysFont("Segoe UI", 20, bold=True)
    header_font = pygame.font.SysFont("Segoe UI", 24, bold=True)

    running = True
    while running:
        screen.fill(DARK_BG)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    active_view = 1
                elif event.key == pygame.K_2:
                    active_view = 2
                elif event.key == pygame.K_3:
                    active_view = 3
                elif event.key == pygame.K_UP:
                    health_score = min(0.85, health_score + 0.05)
                    rul_cycles = max(0, rul_cycles - 12)
                elif event.key == pygame.K_DOWN:
                    health_score = 0.42
                    rul_cycles = 100

        # Status Logic
        if health_score < 0.48:
            status_text, status_color = "HEALTHY", GREEN
        elif health_score < 0.58:
            status_text, status_color = "WARNING (Spall Detected)", YELLOW
        else:
            status_text, status_color = "CRITICAL (CMMS Dispatched)", RED

        # Generate Telemetry Waveform
        noise_amp = (health_score - 0.35) * 50
        wave_history.append(random.uniform(-noise_amp, noise_amp))
        if len(wave_history) > 150:
            wave_history.pop(0)

        # Top Navigation Bar
        pygame.draw.rect(screen, PANEL_BG, (10, 10, 980, 50), border_radius=6)
        lbl1 = bold_font.render("[1] Physical Digital Twin", True, BLUE if active_view == 1 else TEXT_COLOR)
        lbl2 = bold_font.render("[2] FFT Frequency Spectrum", True, BLUE if active_view == 2 else TEXT_COLOR)
        lbl3 = bold_font.render("[3] CMMS & Financial ROI", True, BLUE if active_view == 3 else TEXT_COLOR)
        screen.blit(lbl1, (30, 22))
        screen.blit(lbl2, (340, 22))
        screen.blit(lbl3, (680, 22))

        # View 1: Physical Digital Twin & Oscilloscope
        if active_view == 1:
            pygame.draw.rect(screen, PANEL_BG, (10, 70, 480, 460), border_radius=8)
            t1 = header_font.render("BEARING GEOMETRY & WEAR", True, CYAN)
            screen.blit(t1, (30, 85))
            draw_bearing_digital_twin(screen, (250, 310), health_score)

            pygame.draw.rect(screen, PANEL_BG, (500, 70, 490, 460), border_radius=8)
            t2 = header_font.render("20kHz VIBRATION OSCILLOSCOPE", True, CYAN)
            screen.blit(t2, (520, 85))

            # Telemetry text
            screen.blit(font.render(f"Isolation Forest Score: {health_score:.2f}", True, TEXT_COLOR), (520, 130))
            screen.blit(font.render(f"Projected RUL: {rul_cycles} Cycles", True, TEXT_COLOR), (520, 160))
            screen.blit(bold_font.render(f"Regime: {status_text}", True, status_color), (520, 190))

            # Waveform Plot
            pygame.draw.rect(screen, DARK_BG, (520, 240, 450, 260), border_radius=6)
            pts = [(520 + idx * 3, 370 + val) for idx, val in enumerate(wave_history)]
            if len(pts) > 1:
                pygame.draw.lines(screen, status_color, False, pts, 2)

        # View 2: FFT Frequency Spectrum Monitor
        elif active_view == 2:
            pygame.draw.rect(screen, PANEL_BG, (10, 70, 980, 460), border_radius=8)
            t1 = header_font.render("FAST FOURIER TRANSFORM (FFT) SPECTRAL ANALYSIS", True, CYAN)
            screen.blit(t1, (30, 85))
            screen.blit(font.render("Isolating Outer Race Defect Harmonic (BPFO = 236.4 Hz)", True, TEXT_COLOR), (30, 115))

            # Render FFT Graph Area
            pygame.draw.rect(screen, DARK_BG, (30, 150, 920, 350), border_radius=6)
            
            # Baseline Noise Floor
            fft_pts = []
            for x_pos in range(30, 950, 5):
                amplitude = random.uniform(5, 20)
                # Spike at BPFO frequency marker when degraded
                if 420 <= x_pos <= 450 and health_score >= 0.48:
                    amplitude += (health_score - 0.40) * 450
                fft_pts.append((x_pos, 470 - amplitude))

            if len(fft_pts) > 1:
                pygame.draw.lines(screen, status_color, False, fft_pts, 2)

            # BPFO Marker
            pygame.draw.line(screen, RED, (435, 160), (435, 470), 1)
            screen.blit(bold_font.render("BPFO Defect Peak (236Hz)", True, RED), (370, 160))

        # View 3: CMMS Webhook Dispatcher & Financial ROI
        elif active_view == 3:
            pygame.draw.rect(screen, PANEL_BG, (10, 70, 480, 460), border_radius=8)
            screen.blit(header_font.render("AUTOMATED CMMS DISPATCH", True, CYAN) , (30, 85))
            
            # JSON Payload Visualizer
            pygame.draw.rect(screen, DARK_BG, (30, 130, 440, 380), border_radius=6)
            json_text = [
                "{",
                '  "event": "CRITICAL_ANOMALY",',
                '  "asset": "IMS_BEARING_01",',
                f'  "anomaly_score": {health_score:.2f},',
                f'  "projected_rul": {rul_cycles},',
                f'  "status": "{status_text}",',
                '  "target_api": "https://sap.plant.internal/api/v1/workorder",',
                '  "http_status": "' + ("201 CREATED" if health_score >= 0.58 else "STANDBY") + '"',
                "}"
            ]
            for idx, line in enumerate(json_text):
                color = GREEN if "201" in line else (RED if "CRITICAL" in line else TEXT_COLOR)
                screen.blit(font.render(line, True, color), (45, 150 + idx * 30))

            pygame.draw.rect(screen, PANEL_BG, (500, 70, 490, 460), border_radius=8)
            screen.blit(header_font.render("FINANCIAL ROI ENGINE", True, CYAN), (520, 85))
            screen.blit(font.render("Quantified Downtime Cost Savings", True, TEXT_COLOR), (520, 120))
            
            # Big ROI Dollar Display
            pygame.draw.rect(screen, DARK_BG, (520, 170, 450, 120), border_radius=6)
            roi_display = f"${total_roi_saved:,.2f}"
            screen.blit(header_font.render(roi_display, True, GREEN), (550, 210))

            screen.blit(font.render("Avoided Catastrophic Failures: 911 Incidents", True, TEXT_COLOR), (520, 320))
            screen.blit(font.render("Mean Time To Dispatch: <150 ms via Webhook", True, TEXT_COLOR), (520, 360))

        # Bottom Instructions Footer
        pygame.draw.rect(screen, PANEL_BG, (10, 540, 980, 50), border_radius=6)
        screen.blit(font.render("Controls: [1] Digital Twin | [2] FFT Spectrum | [3] CMMS Payload | [UP] Degrade | [DOWN] Reset", True, (139, 148, 158)), (30, 555))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()