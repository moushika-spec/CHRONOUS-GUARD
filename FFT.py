import sys
import math
import random
import numpy as np
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# --- Display Config ---
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chronos-Guard: Resource-Constrained Deep Edge Architecture Simulation")
clock = pygame.time.Clock()

# --- Industrial Grey Palette ---
BG_COLOR       = (70, 76, 88)         # Solid Medium Industrial Grey
PANEL_BG       = (32, 38, 50)         # Dark Industrial Surface Panel
BORDER_COLOR   = (110, 125, 150)     # Crisp Slate Panel Borders
PLOT_BG        = (20, 24, 34)         # High-Contrast Plot Fill
TEXT_MAIN      = (255, 255, 255)     # Bright White Header Text
TEXT_MUTED     = (185, 195, 215)     # Readable Slate Labels

# --- Rich Internal Accent Tones ---
ACCENT_BLUE    = (56, 189, 248)       # Core System / Waveform Cyan-Blue
ACCENT_INDIGO  = (99, 102, 241)       # Vibration / FFT High-Frequency Accent
ACCENT_GREEN   = (74, 222, 128)       # Nominal Baseline / RUL Healthy
ACCENT_AMBER   = (251, 191, 36)       # Z-Score Drift / Warnings
ACCENT_RED     = (248, 113, 113)      # Anomaly Detection / Critical Fault
ACCENT_PURPLE  = (192, 132, 252)      # Kurtosis Metric & LLM Stream

# --- Optimized Fonts ---
FONT_TITLE         = pygame.font.SysFont("Segoe UI", 18, bold=True)
FONT_BODY          = pygame.font.SysFont("Segoe UI", 14)
FONT_SMALL         = pygame.font.SysFont("Consolas", 13)
FONT_BOLD          = pygame.font.SysFont("Segoe UI", 14, bold=True)
FONT_SECTION_BIG   = pygame.font.SysFont("Segoe UI", 16, bold=True)
FONT_METRICS_VAL   = pygame.font.SysFont("Segoe UI", 15, bold=True)
FONT_TERMINAL_LOG  = pygame.font.SysFont("Segoe UI Semibold", 15)

# --- Simulation Parameters ---
time_step = 0
bearing_angle = 0.0
fault_injected = False
degradation_level = 0.0

# Time-series Buffer Sizes
MAX_POINTS = 120
vibration_history = [0.0] * MAX_POINTS
z_score_history   = [0.0] * MAX_POINTS
kurtosis_history  = [3.0] * MAX_POINTS
rul_history       = [100.0] * MAX_POINTS

# Telemetry Log Buffer
copilot_logs = [
    "[INFO] Chronos-Guard Deep Edge Core initialized successfully.",
    "[INFO] Localized rolling baseline profiling active (Z-Score & Kurtosis).",
    "[INFO] FFT Spectrum analyzer attached (0-500 Hz Bearing Harmonics)."
]

def add_log(msg):
    global copilot_logs
    copilot_logs.append(msg)
    if len(copilot_logs) > 4:
        copilot_logs.pop(0)

# --- Clean Layout Drawing Helpers ---
def draw_panel(rect, title=""):
    rx, ry, rw, rh = rect
    shadow_rect = pygame.Rect(rx + 2, ry + 3, rw, rh)
    pygame.draw.rect(screen, (45, 50, 60), shadow_rect, border_radius=8)
    
    pygame.draw.rect(screen, PANEL_BG, rect, border_radius=8)
    pygame.draw.rect(screen, BORDER_COLOR, rect, width=1, border_radius=8)
    
    if title:
        lbl = FONT_TITLE.render(title, True, ACCENT_BLUE)
        screen.blit(lbl, (rx + 15, ry + 12))

def draw_bearing(center, radius, health_factor, angle):
    cx, cy = center
    color = ACCENT_GREEN if health_factor < 0.3 else (ACCENT_AMBER if health_factor < 0.7 else ACCENT_RED)
    
    pygame.draw.circle(screen, BORDER_COLOR, center, radius + 12, 5)
    pygame.draw.circle(screen, color, center, radius, 3)
    
    pygame.draw.circle(screen, PLOT_BG, center, radius - 24)
    pygame.draw.circle(screen, BORDER_COLOR, center, radius - 24, 2)
    
    num_balls = 8
    for i in range(num_balls):
        theta = angle + i * (2 * math.pi / num_balls)
        bx = int(cx + (radius - 12) * math.cos(theta))
        by = int(cy + (radius - 12) * math.sin(theta))
        ball_color = (226, 232, 240)
        if health_factor > 0.4 and i % 3 == 0:
            ball_color = ACCENT_RED if health_factor > 0.7 else ACCENT_AMBER
        pygame.draw.circle(screen, ball_color, (bx, by), 7)
        pygame.draw.circle(screen, (15, 23, 42), (bx, by), 7, 1)

def draw_plot(rect, data, color, min_val, max_val, label="", label_y_offset=6):
    x, y, w, h = rect
    plot_bg = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, PLOT_BG, plot_bg, border_radius=6)
    pygame.draw.rect(screen, BORDER_COLOR, plot_bg, width=1, border_radius=6)
    
    if label:
        txt = FONT_SMALL.render(f"{label}: {data[-1]:.2f}", True, TEXT_MAIN)
        screen.blit(txt, (x + 10, y + label_y_offset))
    
    if len(data) < 2:
        return
    
    points = []
    for i, val in enumerate(data):
        px = x + 10 + (i / (MAX_POINTS - 1)) * (w - 20)
        norm_val = (val - min_val) / (max_val - min_val + 1e-6)
        norm_val = max(0.0, min(1.0, norm_val))
        py = y + h - 8 - (norm_val * (h - 18))
        points.append((px, py))
    
    pygame.draw.lines(screen, color, False, points, 2)

def draw_fft_bars(rect, signal_buffer, is_fault, deg_level):
    """Computes and renders Fast Fourier Transform (FFT) spectrum bars."""
    x, y, w, h = rect
    plot_bg = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, PLOT_BG, plot_bg, border_radius=6)
    pygame.draw.rect(screen, BORDER_COLOR, plot_bg, width=1, border_radius=6)

    # Compute FFT
    fft_vals = np.abs(np.fft.rfft(signal_buffer))
    num_bins = min(28, len(fft_vals))
    fft_sub = fft_vals[:num_bins]
    
    # Scale FFT Bins
    max_fft = np.max(fft_sub) + 1e-5
    
    lbl = FONT_SMALL.render("FFT Frequency Spectrum (0-500 Hz)", True, TEXT_MAIN)
    screen.blit(lbl, (x + 10, y + 5))

    bar_width = (w - 20) / num_bins
    for i in range(num_bins):
        bx = x + 10 + i * bar_width
        norm_h = min(1.0, fft_sub[i] / (max_fft if not is_fault else 18.0))
        bh = norm_h * (h - 26)
        by = y + h - bh - 5
        
        # Color coding: Highlight fault harmonic spikes in Indigo/Purple or Amber
        if is_fault and (i == 7 or i == 14 or i == 21):  # Simulated BPFO/BPFI bearing fault peaks
            bar_color = ACCENT_RED if deg_level > 0.6 else ACCENT_AMBER
        else:
            bar_color = ACCENT_INDIGO

        pygame.draw.rect(screen, bar_color, (bx + 1, by, max(2, bar_width - 2), bh), border_radius=2)

# --- Main Game Loop ---
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Frame time in seconds
    
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fault_injected = not fault_injected
                if fault_injected:
                    add_log("[ALERT] Bearing Fault Injected! FFT Harmonics Rising (BPFO Peak).")
                else:
                    add_log("[INFO] Fault cleared. Recalibrating baseline...")
                    degradation_level = 0.0
            elif event.key == pygame.K_r:
                degradation_level = 0.0
                fault_injected = False
                vibration_history = [0.0] * MAX_POINTS
                z_score_history   = [0.0] * MAX_POINTS
                kurtosis_history  = [3.0] * MAX_POINTS
                rul_history       = [100.0] * MAX_POINTS
                add_log("[INFO] Edge Engine Reset to nominal state.")

    # --- Physics & Signal Generation ---
    time_step += dt
    bearing_angle += 2.5 * dt
    
    if fault_injected:
        degradation_level = min(1.0, degradation_level + 0.0012)
    
    base_freq = 25.0
    harmonic = math.sin(2 * math.pi * base_freq * time_step)
    noise = random.gauss(0, 0.12 + degradation_level * 0.35)
    
    spall_impulse = 0.0
    if fault_injected and random.random() < (0.12 + degradation_level * 0.45):
        spall_impulse = random.choice([-1, 1]) * (1.8 + degradation_level * 4.5)
        
    vib_signal = harmonic * 0.25 + noise + spall_impulse
    vibration_history.append(vib_signal)
    vibration_history.pop(0)

    # --- Edge Analytics ---
    recent_vib = vibration_history[-30:]
    mean_v = np.mean(recent_vib)
    std_v = np.std(recent_vib) + 1e-5
    
    z_score = abs((vib_signal - mean_v) / std_v)
    z_score_history.append(z_score)
    z_score_history.pop(0)

    kurtosis_val = np.mean(((recent_vib - mean_v) / std_v) ** 4)
    kurtosis_history.append(kurtosis_val)
    kurtosis_history.pop(0)

    raw_anomaly = (kurtosis_val - 3.0) / 10.0 + (z_score / 5.5)
    anomaly_score = max(0.0, min(1.0, raw_anomaly))

    current_rul = max(0.0, rul_history[-1] - (anomaly_score * 0.18 if anomaly_score > 0.25 else -0.04))
    current_rul = min(100.0, current_rul)
    rul_history.append(current_rul)
    rul_history.pop(0)

    if anomaly_score > 0.70 and random.random() < 0.015:
        add_log(f"[COPILOT ALERT] High FFT Harmonic Peak & Kurtosis ({kurtosis_val:.1f}). Inspect Bearing.")
    elif z_score > 3.8 and random.random() < 0.015:
        add_log(f"[COPILOT ALERT] Z-Score Drift: {z_score:.2f}. RUL decaying.")

    # --- Render Screen ---
    screen.fill(BG_COLOR)

    # --- Header Section ---
    hdr = FONT_TITLE.render("CHRONOS-GUARD: Deep Edge Architecture for Predictive Maintenance", True, TEXT_MAIN)
    sub = FONT_BODY.render("NASA IMS Bearing Dataset Simulation | Zero Cloud Latency Pipeline", True, TEXT_MUTED)
    screen.blit(hdr, (18, 12))
    screen.blit(sub, (18, 34))

    # Control Instructions Pill
    ctrl_bg = pygame.Rect(WIDTH - 355, 14, 338, 34)
    pygame.draw.rect(screen, PANEL_BG, ctrl_bg, border_radius=6)
    pygame.draw.rect(screen, BORDER_COLOR, ctrl_bg, width=1, border_radius=6)
    ctrl_txt = FONT_BODY.render("[SPACE] Toggle Fault  |  [R] Reset Engine", True, ACCENT_AMBER)
    screen.blit(ctrl_txt, (WIDTH - 343, 21))

    # ================= FITTED LAYOUT GRID =================
    
    # 1. Physical Asset Twin Panel (Left Top)
    draw_panel((18, 60, 310, 270), "Physical Asset Twin")
    draw_bearing((173, 175), 62, degradation_level, bearing_angle)
    
    status_str = "HEALTHY" if degradation_level < 0.3 else ("DEGRADED" if degradation_level < 0.7 else "CRITICAL")
    status_col = ACCENT_GREEN if degradation_level < 0.3 else (ACCENT_AMBER if degradation_level < 0.7 else ACCENT_RED)
    
    screen.blit(FONT_BOLD.render(f"Asset State: {status_str}", True, status_col), (34, 260))
    screen.blit(FONT_BODY.render(f"Degradation Level: {degradation_level * 100:.1f}%", True, TEXT_MAIN), (34, 288))

    # 2. Edge Feature Extraction Panel (Middle Top - NOW WITH FFT SPECTRUM)
    draw_panel((340, 60, 440, 270), "Edge Feature Extraction")
    draw_plot((355, 96, 410, 76), vibration_history, ACCENT_BLUE, -5.0, 5.0, "Vibration Waveform (g)")
    draw_plot((355, 178, 410, 76), z_score_history, ACCENT_AMBER, 0.0, 6.0, "Rolling Z-Score Baseline")
    draw_fft_bars((355, 258, 410, 64), vibration_history, fault_injected, degradation_level)

    # 3. Unsupervised Anomaly & RUL Core Panel (Right Top)
    draw_panel((792, 60, 470, 270), "Unsupervised Anomaly & RUL Core")
    draw_plot((808, 98, 438, 95), kurtosis_history, ACCENT_PURPLE, 0.0, 15.0, "Windowed Kurtosis Metric")
    
    rul_lbl = FONT_SMALL.render(f"Remaining Useful Life (RUL %): {rul_history[-1]:.2f}", True, TEXT_MAIN)
    screen.blit(rul_lbl, (820, 198))
    draw_plot((808, 224, 438, 73), rul_history, ACCENT_GREEN if current_rul > 40 else ACCENT_RED, 0.0, 100.0, label="", label_y_offset=0)

    # 4. Bottom Row: Asynchronous Telemetry Stream & LLM Maintenance Copilot
    draw_panel((18, 342, 1244, 358), "Asynchronous Telemetry Stream & LLM Maintenance Copilot")
    
    # Edge Summary Card
    summary_box = pygame.Rect(34, 385, 310, 298)
    pygame.draw.rect(screen, PLOT_BG, summary_box, border_radius=6)
    pygame.draw.rect(screen, BORDER_COLOR, summary_box, width=1, border_radius=6)
    
    screen.blit(FONT_SECTION_BIG.render("Edge Diagnostic Metrics", True, ACCENT_BLUE), (48, 405))
    screen.blit(FONT_METRICS_VAL.render(f"• Kurtosis Index: {kurtosis_val:.2f} (Norm: 3.0)", True, TEXT_MAIN), (48, 450))
    screen.blit(FONT_METRICS_VAL.render(f"• Anomaly Score: {anomaly_score:.3f}", True, TEXT_MAIN), (48, 495))
    screen.blit(FONT_METRICS_VAL.render(f"• Estimated RUL: {current_rul:.1f} Cycles", True, TEXT_MAIN), (48, 540))
    screen.blit(FONT_METRICS_VAL.render(f"• Cloud Overhead: ~0.6 KB/s (Optimized)", True, ACCENT_GREEN), (48, 585))

    # Live Copilot Terminal Feed
    terminal_box = pygame.Rect(358, 385, 888, 298)
    pygame.draw.rect(screen, PLOT_BG, terminal_box, border_radius=6)
    pygame.draw.rect(screen, BORDER_COLOR, terminal_box, width=1, border_radius=6)
    
    screen.blit(FONT_SECTION_BIG.render("Live Telemetry Stream -> LLM Maintenance Copilot", True, ACCENT_PURPLE), (378, 405))
    pygame.draw.line(screen, BORDER_COLOR, (378, 434), (1226, 434), 1)

    for idx, log in enumerate(copilot_logs):
        col = ACCENT_RED if "ALERT" in log else (ACCENT_AMBER if "Injected" in log else TEXT_MAIN)
        t_surf = FONT_TERMINAL_LOG.render(log, True, col)
        screen.blit(t_surf, (378, 452 + idx * 44))

    pygame.display.flip()

pygame.quit() 
sys.exit()