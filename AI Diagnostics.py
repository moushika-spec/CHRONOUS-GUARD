# CHRONOUS-GUARD | High-Visibility Mission Control Telemetry Deck
import math 
import os
import random
import sys
import traceback

try:
  import pygame
  from collections import deque
  import numpy as np 
  import pandas as pd

  # Initialize Pygame safely
  pygame.init()
  pygame.font.init()

  # Window Configuration (720p Optimized)
  WIDTH, HEIGHT = 1280, 720
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("CHRONOUS-GUARD | Advanced Mission Control Deck")

  # Modern Industrial Charcoal & Slate Palette
  BG_COLOR = (22, 26, 34)       # Sleek Industrial Charcoal Background
  PANEL_BG = (30, 36, 46)       # Slate Card Panel Background
  BORDER_COLOR = (70, 90, 120)  # Distinct Tactical Border
  TEXT_BRIGHT = (255, 255, 255)
  TEXT_DIM = (180, 195, 220)
  
  COLOR_CYAN = (0, 229, 255)    # Holographic Cyan
  COLOR_EMERALD = (46, 204, 113)# Healthy Green
  COLOR_AMBER = (241, 196, 15)  # Warning Yellow
  COLOR_CRITICAL = (231, 76, 60)# Fault Red
  COLOR_PURPLE = (155, 89, 182)

  # Guaranteed Safe Font Loader
  def get_font(size, bold=False):
    for name in ["Noto Serif Condensed", "Noto Serif", "Georgia", "Arial"]:
      try:
        f = pygame.font.SysFont(name, size, bold=bold)
        if f: return f
      except: pass
    return pygame.font.Font(None, size + 6)

  # Significantly Increased Font Sizes for Maximum Visibility
  FONT_TITLE = get_font(30, bold=False)
  FONT_SECTION = get_font(24, bold=False)
  FONT_HUD = get_font(24, bold=False)
  FONT_SMALL = get_font(22, bold=False)

  # Generate Simulated Telemetry Data (400 Frames)
  n = 400
  cycles = np.arange(1, n + 1)
  vib = 0.03 * np.exp(cycles * 0.008) + np.random.normal(0, 0.012, n)
  kurt = 3.0 + vib * 4.5 + np.random.normal(0, 0.05, n)
  health = np.clip(100 - (vib / max(vib.max(), 0.1) * 90), 0, 100)
  status = np.where(health > 70, "NORMAL", np.where(health > 35, "WARNING", "CRITICAL"))
  rul = np.clip(health * 1.5, 0, 150)
  anomaly_scores = np.clip(0.3 + (100 - health) * 0.005 + np.random.normal(0, 0.02, n), 0.1, 0.95)
  fft_fault_bin = np.random.randint(120, 320, n)

  trend_deque = deque(maxlen=100)
  clock = pygame.time.Clock()
  idx = 0
  paused = False
  radar_angle = 0.0

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE: paused = not paused
        elif event.key == pygame.K_RIGHT: idx = min(n - 1, idx + 5)
        elif event.key == pygame.K_LEFT: idx = max(0, idx - 5)

    # Fetch current frame telemetry
    v = float(vib[idx])
    k = float(kurt[idx])
    h = float(health[idx])
    r = float(rul[idx])
    st = str(status[idx])
    anomaly = float(anomaly_scores[idx])
    fft_val = int(fft_fault_bin[idx])
    
    crest_factor = round(3.0 + (v * 12.5), 2)
    thermal_temp = round(42.5 + (v * 35.0), 1)
    dom_freq = int(fft_val * 1.5)

    trend_deque.append(v)

    if st == "CRITICAL": scolor = COLOR_CRITICAL
    elif st == "WARNING": scolor = COLOR_AMBER
    else: scolor = COLOR_EMERALD

    screen.fill(BG_COLOR)

    # ==========================================================
    # LEFT PANEL: Holographic Sensor Radar & Topology Matrix
    # ==========================================================
    lx, ly, lw, lh = 20, 20, 520, 680
    pygame.draw.rect(screen, PANEL_BG, (lx, ly, lw, lh), border_radius=12)
    pygame.draw.rect(screen, BORDER_COLOR, (lx, ly, lw, lh), width=2, border_radius=12)

    screen.blit(FONT_TITLE.render("📡 MULTI-CHANNEL SENSOR TOPOLOGY", True, COLOR_CYAN), (lx + 20, ly + 20))
    pygame.draw.line(screen, BORDER_COLOR, (lx + 20, ly + 60), (lx + lw - 20, ly + 60), 1)

    # Central Radar Sweep Area
    rx, ry, r_radius = lx + lw // 2, ly + 210, 115
    
    for r_step in [30, 60, 90, 115]:
      pygame.draw.circle(screen, (45, 58, 78), (rx, ry), r_step, 1)

    pygame.draw.line(screen, (45, 58, 78), (rx - r_radius, ry), (rx + r_radius, ry), 1)
    pygame.draw.line(screen, (45, 58, 78), (rx, ry - r_radius), (rx, ry + r_radius), 1)

    radar_angle += 0.03
    sweep_x = rx + int(r_radius * math.cos(radar_angle))
    sweep_y = ry + int(r_radius * math.sin(radar_angle))
    pygame.draw.line(screen, COLOR_CYAN, (rx, ry), (sweep_x, sweep_y), 2)
    pygame.draw.circle(screen, scolor, (rx, ry), 55, 3)

    num_nodes = 8
    for i in range(num_nodes):
      ang = (i * (2 * math.pi / num_nodes)) + (radar_angle * 0.2)
      dist = 80 + int(math.sin(radar_angle + i) * 10)
      nx = rx + int(dist * math.cos(ang))
      ny = ry + int(dist * math.sin(ang))
      
      pygame.draw.circle(screen, scolor, (nx, ny), 11)
      pygame.draw.circle(screen, TEXT_BRIGHT, (nx, ny), 11, 2)
      pygame.draw.line(screen, (60, 80, 110), (rx, ry), (nx, ny), 1)

    # Isolation Forest Anomaly Probability Gauge
    gauge_y = ly + 360
    screen.blit(FONT_SECTION.render("Isolation Forest Outlier Probability", True, TEXT_DIM), (lx + 20, gauge_y))
    
    bar_x, bar_y, bar_w, bar_h = lx + 20, gauge_y + 32, lw - 40, 28
    pygame.draw.rect(screen, (18, 22, 28), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
    fill_width = int(bar_w * anomaly)
    pygame.draw.rect(screen, scolor, (bar_x, bar_y, fill_width, bar_h), border_radius=6)
    pygame.draw.rect(screen, BORDER_COLOR, (bar_x, bar_y, bar_w, bar_h), width=1, border_radius=6)
    
    anom_text = FONT_HUD.render(f"Anomaly Outlier Score: {anomaly:.3f} ({st})", True, TEXT_BRIGHT)
    screen.blit(anom_text, (bar_x + 12, bar_y + 3))

    # Additional Diagnostic Badges
    info_y = ly + 460
    screen.blit(FONT_HUD.render(f"Thermal Index: {thermal_temp} °C", True, COLOR_AMBER), (lx + 20, info_y))
    screen.blit(FONT_HUD.render(f"Crest Factor: {crest_factor} g", True, COLOR_CYAN), (lx + 20, info_y + 42))
    screen.blit(FONT_HUD.render(f"Dominant Freq: {dom_freq} Hz", True, TEXT_BRIGHT), (lx + 20, info_y + 84))


    # ==========================================================
    # RIGHT PANEL: Telemetry Deck & Real-Time Analytics Charts
    # ==========================================================
    hx, hy, hw, hh = 560, 20, 700, 680
    pygame.draw.rect(screen, PANEL_BG, (hx, hy, hw, hh), border_radius=12)
    pygame.draw.rect(screen, BORDER_COLOR, (hx, hy, hw, hh), width=2, border_radius=12)

    screen.blit(FONT_TITLE.render("🛡️ CHRONOUS-GUARD AI DIAGNOSTICS", True, COLOR_CYAN), (hx + 20, hy + 20))
    pygame.draw.line(screen, BORDER_COLOR, (hx + 20, hy + 60), (hx + hw - 20, hy + 60), 1)

    metrics = [
        ("Execution Cycle:", f"{idx + 1} / {n}", TEXT_BRIGHT),
        ("Asset Health Status:", st, scolor),
        ("Equipment Health Index:", f"{h:.1f}%", COLOR_CYAN),
        ("Remaining Useful Life (RUL):", f"{r:.1f} Cycles", COLOR_AMBER),
        ("Vibration RMS Stress:", f"{v:.4f} g", TEXT_BRIGHT),
        ("Windowed Kurtosis Index:", f"{k:.2f}", COLOR_CRITICAL if k > 5.0 else TEXT_BRIGHT),
    ]

    y_off = hy + 75
    for label, val, col in metrics:
      lbl_surf = FONT_HUD.render(label, True, TEXT_DIM)
      val_surf = FONT_HUD.render(val, True, col)
      screen.blit(lbl_surf, (hx + 25, y_off))
      screen.blit(val_surf, (hx + 410, y_off))
      y_off += 35

    # --- REAL-TIME VIBRATION TREND GRAPH ---
    gx, gy, gw, gh = hx + 25, hy + 300, 650, 140
    pygame.draw.rect(screen, (18, 22, 28), (gx, gy, gw, gh), border_radius=8)
    pygame.draw.rect(screen, BORDER_COLOR, (gx, gy, gw, gh), width=1, border_radius=8)
    screen.blit(FONT_SECTION.render("Real-Time Vibration Waveform & Stress Trend (g)", True, COLOR_CYAN), (gx + 15, gy + 10))

    if len(trend_deque) > 1:
      points = []
      max_v = max(max(trend_deque), 0.1)
      for i, val in enumerate(trend_deque):
        px = gx + 15 + int(i * (gw - 30) / 100)
        py = gy + gh - 15 - int((val / (max_v * 1.4)) * (gh - 45))
        points.append((px, py))
      pygame.draw.lines(screen, COLOR_EMERALD, False, points, 2)

    # --- FFT SPECTRAL FREQUENCY SPECTRUM --- 
    fx, fy, fw, fh = hx + 25, hy + 455, 650, 130
    pygame.draw.rect(screen, (18, 22, 28), (fx, fy, fw, fh), border_radius=8)
    pygame.draw.rect(screen, BORDER_COLOR, (fx, fy, fw, fh), width=1, border_radius=8)
    screen.blit(FONT_SECTION.render("FFT Frequency Spectrum & Harmonic Spikes (Hz)", True, COLOR_CYAN), (fx + 15, fy + 10))

    bin_w = (fw - 30) // 50
    for b in range(50):
      spike_h = int(random.uniform(4, 12) + (22 if b in [12, 28, 41] else 0))
      bar_color = COLOR_PURPLE if b not in [12, 28, 41] else COLOR_CRITICAL
      pygame.draw.rect(screen, bar_color, (fx + 15 + b * bin_w, fy + fh - 12 - spike_h * 2.2, bin_w - 2, spike_h * 2.2), border_radius=2)

    # AI Recommendation Banner
    rec_text = "• AI Recommendation: Operational parameters nominal."
    if st == "WARNING": rec_text = "• AI Recommendation: Outer raceway degradation detected. Schedule inspection."
    if st == "CRITICAL": rec_text = "• AI Recommendation: Severe fault frequency harmonic! Immediate shutdown advised."
    
    screen.blit(FONT_SMALL.render(rec_text, True, scolor), (hx + 25, hy + 595))

    # Controls Footer
    ctrl_text = FONT_SMALL.render("[SPACE]: Pause  |  [<-- / -->]: Step Frames  |  [ESC]: Exit Deck", True, TEXT_DIM)
    screen.blit(ctrl_text, (hx + 25, hy + hh - 35))

    if not paused:
      idx = (idx + 1) % n

    pygame.display.flip()
    clock.tick(30)

  pygame.quit()
  sys.exit()

except Exception as err:
  print(f"Error: {err}")
  with open("error_log.txt", "w") as f:
    traceback.print_exc(file=f)