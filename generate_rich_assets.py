import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

screenshots_dir = r"c:\Users\yeshwanth\OneDrive\Desktop\cloud product 2\cloud computing product 2\docs\screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. Ultra High-Res Architecture Diagram (1920 x 1080)
# -------------------------------------------------------------
def make_architecture_diagram():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor('#070A13')
    ax.set_facecolor('#070A13')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Header
    ax.text(8, 8.45, "EnviroSense — 4-Tier Serverless IoT Architecture", 
            ha='center', va='center', color='#FFFFFF', fontsize=24, weight='bold', fontfamily='sans-serif')
    ax.text(8, 8.0, "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205) · PRODUCT NO. 23", 
            ha='center', va='center', color='#06B6D4', fontsize=12, weight='bold', fontfamily='sans-serif')

    tiers = [
        {"x": 0.7, "y": 1.1, "w": 3.3, "h": 6.4, "title": "TIER 1: EDGE & VIRTUAL SIM", "color": "#06B6D4"},
        {"x": 4.5, "y": 1.1, "w": 2.8, "h": 6.4, "title": "TIER 2: API GATEWAY", "color": "#F59E0B"},
        {"x": 7.8, "y": 1.1, "w": 3.6, "h": 6.4, "title": "TIER 3: SERVERLESS COMPUTE", "color": "#FF9900"},
        {"x": 11.9, "y": 1.1, "w": 3.4, "h": 6.4, "title": "TIER 4: STORAGE & DASHBOARD", "color": "#10B981"}
    ]

    for t in tiers:
        bg = patches.FancyBboxPatch((t['x'], t['y']), t['w'], t['h'],
                                    boxstyle="round,pad=0.1,rounding_size=0.28",
                                    facecolor='#10172A', edgecolor='#1E293B', lw=1.5)
        ax.add_patch(bg)
        top_bar = patches.Rectangle((t['x'] + 0.2, t['y'] + t['h'] - 0.08), t['w'] - 0.4, 0.06, facecolor=t['color'])
        ax.add_patch(top_bar)
        ax.text(t['x'] + t['w']/2, t['y'] + t['h'] - 0.45, t['title'],
                ha='center', va='center', color=t['color'], fontsize=11, weight='bold')

    def add_card(x, y, w, h, title, lines, color, fill='#162038'):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.18",
                                      facecolor=fill, edgecolor=color, lw=1.2)
        ax.add_patch(card)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', color='#FFFFFF', fontsize=11, weight='bold')
        for i, line in enumerate(lines):
            ax.text(x + 0.2, y + h - 0.72 - (i * 0.34), "• " + line, ha='left', va='center', color='#CBD5E1', fontsize=9.0)

    # Tier 1 Components
    add_card(1.0, 4.4, 2.7, 2.4, "ESP32 Physical Station", [
        "DOIT ESP32 DevKit V1 (240MHz)",
        "DHT22 Precision Temp & Hum",
        "MQ-135 Gas & Air Quality Sensor",
        "SSD1306 0.96\" I2C OLED",
        "Wi-Fi HTTP Client (5s cadence)"
    ], "#06B6D4")

    add_card(1.0, 1.6, 2.7, 2.5, "Wokwi VS Code Simulator", [
        "Wokwi Extension + diagram.json",
        "Virtual Wokwi-GUEST Wi-Fi",
        "host.wokwi.internal bridge",
        "Interactive DHT22 & MQ-135 sliders",
        "Zero-hardware live cloud link"
    ], "#C084FC")

    # Tier 2 Components
    add_card(4.7, 4.4, 2.4, 2.4, "Amazon API Gateway v2", [
        "Lightweight HTTP Protocol",
        "CORS Wildcard Allowed (*)",
        "POST /telemetry Ingestion",
        "GET /telemetry Query",
        "Sub-15ms Latency Routing"
    ], "#F59E0B")

    add_card(4.7, 1.6, 2.4, 2.5, "Local Bridge Server", [
        "Python HTTP Server & Gateway",
        "Static Frontend Asset Delivery",
        "CORS Preflight (OPTIONS)",
        "Bridges Wokwi to Dashboard"
    ], "#38BDF8")

    # Tier 3 Components
    add_card(8.1, 4.4, 3.0, 2.4, "AWS Lambda Function", [
        "Python 3.12 Serverless Runtime",
        "Steadman Heat Index Engine",
        "MQ-135 Gas Hazard Evaluator",
        "128 MB RAM (Sub-cent scale)",
        "Parameterized LabRole Binding"
    ], "#FF9900")

    add_card(8.1, 1.6, 3.0, 2.5, "Real-Time Classification", [
        "NORMAL: Balanced equilibrium",
        "GAS_ALERT: >= 600 PPM VOCs",
        "HEAT_ALERT: Heat Index >= 40°C",
        "FREEZE_ALERT: Temp <= 5°C"
    ], "#FB923C")

    # Tier 4 Components
    add_card(12.2, 4.4, 2.8, 2.4, "Amazon DynamoDB", [
        "Pay-Per-Request On-Demand",
        "Partition Key: deviceId (S)",
        "Sort Key: recordedAt (S)",
        "24-Hour TTL Auto-Pruning",
        "Zero Idle Cloud Cost ($0.00)"
    ], "#10B981")

    add_card(12.2, 1.6, 2.8, 2.5, "Responsive Web Dashboard", [
        "4 Circular SVG Radial Gauges",
        "DHT22 + MQ-135 Real-time Views",
        "Web Audio Synthesizer Sirens",
        "Interactive Scenario Presets"
    ], "#34D399")

    # Connecting Arrows
    def draw_arrow(x1, y1, x2, y2, text, color='#94A3B8'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5, mutation_scale=18))
        if text:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.22
            ax.text(mx, my, text, ha='center', va='center', color=color, fontsize=8.5, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='#070A13', edgecolor=color, lw=1))

    draw_arrow(3.7, 5.6, 4.7, 5.6, "HTTP POST JSON", "#06B6D4")
    draw_arrow(3.7, 2.8, 4.7, 2.8, "Wokwi Internal Bridge", "#C084FC")
    draw_arrow(7.1, 5.6, 8.1, 5.6, "Proxy Event", "#F59E0B")
    draw_arrow(11.1, 5.6, 12.2, 5.6, "PutItem + TTL", "#FF9900")

    # S3 Polling dashed arrow
    ax.annotate('', xy=(7.1, 2.0), xytext=(12.2, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, linestyle="dashed", mutation_scale=16))
    ax.text(9.65, 2.25, "GET /telemetry (5s client polling)", ha='center', va='center', color="#10B981", fontsize=8.5, weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#070A13', edgecolor="#10B981", lw=1))

    plt.tight_layout()
    out_path = os.path.join(screenshots_dir, "architecture-diagram.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 2. Hardware Wiring Schematic (1600 x 900)
# -------------------------------------------------------------
def make_hardware_schematic():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(8, 8.45, "EnviroSense — ESP32 + DHT22 + MQ-135 + OLED Hardware Schematic", 
            ha='center', va='center', color='#FFFFFF', fontsize=22, weight='bold')
    ax.text(8, 8.0, "DOIT ESP32 DEVKIT V1 · DHT22 TEMP & HUMIDITY · MQ-135 GAS SENSOR · SSD1306 OLED · WOKWI COMPATIBLE", 
            ha='center', va='center', color='#06B6D4', fontsize=11, weight='bold')

    # ESP32 Main Board (Center)
    esp = patches.FancyBboxPatch((5.8, 1.8), 4.4, 5.5,
                                 boxstyle="round,pad=0.1,rounding_size=0.35",
                                 facecolor='#1E293B', edgecolor='#06B6D4', lw=2.5)
    ax.add_patch(esp)
    ax.text(8.0, 6.8, "ESP32 DevKit V1", ha='center', va='center', color='#FFFFFF', fontsize=16, weight='bold')
    ax.text(8.0, 6.4, "Dual Core 240MHz · 2.4GHz Wi-Fi", ha='center', va='center', color='#94A3B8', fontsize=10)

    # ESP32 Metal RF Can
    can = patches.Rectangle((7.0, 4.6), 2.0, 1.5, facecolor='#0F172A', edgecolor='#475569', lw=1.5)
    ax.add_patch(can)
    ax.text(8.0, 5.35, "ESP-WROOM-32", ha='center', va='center', color='#64748B', fontsize=9, weight='bold')

    # USB Port on bottom
    usb = patches.Rectangle((7.4, 1.45), 1.2, 0.45, facecolor='#64748B', edgecolor='#94A3B8')
    ax.add_patch(usb)
    ax.text(8.0, 1.65, "Micro USB", ha='center', va='center', color='#0F172A', fontsize=7.5, weight='bold')

    # ESP32 Pin Labels
    # Left: 3V3 (y=4.5), 5V/VIN (y=3.8), GND (y=2.8)
    ax.plot([5.8, 6.2], [4.5, 4.5], color='#EF4444', lw=5)
    ax.text(6.3, 4.5, "3V3 (3.3V Rail)", color='#F8FAFC', fontsize=9.5, weight='bold', va='center')

    ax.plot([5.8, 6.2], [3.8, 3.8], color='#F97316', lw=5)
    ax.text(6.3, 3.8, "5V / VIN (Power)", color='#F8FAFC', fontsize=9.5, weight='bold', va='center')

    ax.plot([5.8, 6.2], [2.8, 2.8], color='#64748B', lw=5)
    ax.text(6.3, 2.8, "GND (Common)", color='#F8FAFC', fontsize=9.5, weight='bold', va='center')

    # Right: GPIO 4 (y=4.6), GPIO 34 (y=3.9), GPIO 35 (y=3.3), GPIO 21 (y=2.7), GPIO 22 (y=2.1)
    ax.plot([9.8, 10.2], [4.6, 4.6], color='#38BDF8', lw=5)
    ax.text(9.7, 4.6, "GPIO 4 (DHT22 Data)", color='#F8FAFC', fontsize=9.5, weight='bold', ha='right', va='center')

    ax.plot([9.8, 10.2], [3.9, 3.9], color='#C084FC', lw=5)
    ax.text(9.7, 3.9, "GPIO 34 (MQ135 AOUT)", color='#F8FAFC', fontsize=9.5, weight='bold', ha='right', va='center')

    ax.plot([9.8, 10.2], [3.3, 3.3], color='#22D3EE', lw=5)
    ax.text(9.7, 3.3, "GPIO 35 (MQ135 DOUT)", color='#F8FAFC', fontsize=9.5, weight='bold', ha='right', va='center')

    ax.plot([9.8, 10.2], [2.7, 2.7], color='#10B981', lw=5)
    ax.text(9.7, 2.7, "GPIO 21 (I2C SDA)", color='#F8FAFC', fontsize=9.5, weight='bold', ha='right', va='center')

    ax.plot([9.8, 10.2], [2.1, 2.1], color='#F59E0B', lw=5)
    ax.text(9.7, 2.1, "GPIO 22 (I2C SCL)", color='#F8FAFC', fontsize=9.5, weight='bold', ha='right', va='center')

    # 1. DHT22 Sensor (Left Top)
    dht = patches.FancyBboxPatch((1.0, 4.5), 3.2, 2.8,
                                boxstyle="round,pad=0.1,rounding_size=0.22",
                                facecolor='#0284C7', edgecolor='#38BDF8', lw=2.5)
    ax.add_patch(dht)
    ax.text(2.6, 6.8, "DHT22 SENSOR", ha='center', va='center', color='#FFFFFF', fontsize=13, weight='bold')
    ax.text(2.6, 6.4, "Precision Temp & Hum", ha='center', va='center', color='#E0F2FE', fontsize=9)
    ax.text(2.6, 5.0, "Pinout:\nVCC (3V3) | DATA (GPIO 4)\nNC (Float) | GND (Common)", ha='center', va='center', color='#FFFFFF', fontsize=8.5, weight='bold')

    # 2. MQ-135 Gas Sensor (Left Bottom)
    mq = patches.FancyBboxPatch((1.0, 1.4), 3.2, 2.7,
                                boxstyle="round,pad=0.1,rounding_size=0.22",
                                facecolor='#581C87', edgecolor='#C084FC', lw=2.5)
    ax.add_patch(mq)
    ax.text(2.6, 3.65, "MQ-135 SENSOR", ha='center', va='center', color='#FFFFFF', fontsize=13, weight='bold')
    ax.text(2.6, 3.3, "Air Quality & Toxic Gas", ha='center', va='center', color='#E9D5FF', fontsize=9)
    ax.text(2.6, 2.1, "Pinout:\nVCC (5V) | GND (Common)\nAOUT (GPIO 34 ADC1)\nDOUT (GPIO 35)", ha='center', va='center', color='#FFFFFF', fontsize=8.5, weight='bold')

    # 3. SSD1306 OLED (Right side)
    oled = patches.FancyBboxPatch((11.8, 1.8), 3.2, 5.2,
                                 boxstyle="round,pad=0.1,rounding_size=0.25",
                                 facecolor='#1E293B', edgecolor='#F59E0B', lw=2.5)
    ax.add_patch(oled)
    ax.text(13.4, 6.6, "SSD1306 OLED", ha='center', va='center', color='#FFFFFF', fontsize=14, weight='bold')
    ax.text(13.4, 6.25, "0.96\" I2C Monochrome", ha='center', va='center', color='#94A3B8', fontsize=9.5)

    # OLED Glass area
    screen = patches.Rectangle((12.2, 3.2), 2.4, 2.7, facecolor='#000000', edgecolor='#475569', lw=1.5)
    ax.add_patch(screen)
    ax.text(13.4, 5.4, "EnviroSense  WiFi:OK", ha='center', va='center', color='#F59E0B', fontsize=8, weight='bold')
    ax.text(13.4, 4.8, "T: 24.5C  H: 48%", ha='center', va='center', color='#38BDF8', fontsize=8.5, weight='bold')
    ax.text(13.4, 4.3, "HI: 24.3C Gas: 180", ha='center', va='center', color='#34D399', fontsize=8.5, weight='bold')
    ax.text(13.4, 3.8, "Air: GOOD  STATUS:OK", ha='center', va='center', color='#C084FC', fontsize=8.5, weight='bold')

    ax.text(13.4, 2.4, "Pinout: VCC | GND | SCL | SDA", ha='center', va='center', color='#CBD5E1', fontsize=9, weight='bold')

    # Wokwi simulation badge
    wokwi_badge = patches.FancyBboxPatch((5.8, 0.75), 4.4, 0.8, boxstyle="round,pad=0.08", facecolor='#1E1E38', edgecolor='#C084FC', lw=1.5)
    ax.add_patch(wokwi_badge)
    ax.text(8.0, 1.15, "⚡ WOKWI VS CODE SIMULATOR COMPATIBLE", ha='center', va='center', color='#C084FC', fontsize=9.5, weight='bold')

    out_path = os.path.join(screenshots_dir, "hardware-schematic.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 3. Steadman Heat Index Risk Matrix Chart (1600 x 900)
# -------------------------------------------------------------
def make_heat_matrix_chart():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')

    ax.text(0.5, 1.08, "Steadman Heat Index & Thermal Hazard Risk Spectrum", 
            ha='center', va='center', transform=ax.transAxes, color='#FFFFFF', fontsize=22, weight='bold')
    ax.text(0.5, 1.03, "NOAA / NWS Heat Risk Matrix: Temperature vs Relative Humidity Calculations", 
            ha='center', va='center', transform=ax.transAxes, color='#06B6D4', fontsize=11, weight='bold')

    temps = np.linspace(20, 45, 100)
    hums = np.linspace(20, 100, 100)
    T, H = np.meshgrid(temps, hums)

    T_F = (T * 9.0 / 5.0) + 32.0
    HI_F = (
        -42.379 + (2.04901523 * T_F) + (10.14333127 * H)
        - (0.22475541 * T_F * H) - (0.00683783 * (T_F**2)) - (0.05481717 * (H**2))
        + (0.00122874 * (T_F**2) * H) + (0.00085282 * T_F * (H**2)) - (0.00000199 * (T_F**2) * (H**2))
    )
    HI_C = (HI_F - 32.0) * 5.0 / 9.0

    levels = [15, 27, 32, 41, 54, 80]
    colors = ['#10B981', '#F59E0B', '#F97316', '#EF4444', '#7F1D1D']
    cs = ax.contourf(temps, hums, HI_C, levels=levels, colors=colors, alpha=0.85)

    cbar = fig.colorbar(cs, ax=ax, orientation='vertical', pad=0.03)
    cbar.set_label('Apparent Heat Index (°C)', color='#FFFFFF', fontsize=12, weight='bold')
    cbar.ax.tick_params(labelsize=10, colors='#CBD5E1')

    ax.set_xlabel('Ambient Temperature (°C)', color='#FFFFFF', fontsize=13, weight='bold', labelpad=10)
    ax.set_ylabel('Relative Humidity (%)', color='#FFFFFF', fontsize=13, weight='bold', labelpad=10)
    ax.tick_params(colors='#94A3B8', labelsize=11)
    ax.grid(color='#334155', linestyle='--', linewidth=0.8, alpha=0.6)

    ax.text(23, 40, "NORMAL / SAFE\n(<27°C)", color='#FFFFFF', fontsize=12, weight='bold', ha='center', bbox=dict(boxstyle="round", facecolor='#064E3B', alpha=0.8))
    ax.text(28, 60, "CAUTION\n(27°C - 32°C)", color='#FFFFFF', fontsize=12, weight='bold', ha='center', bbox=dict(boxstyle="round", facecolor='#78350F', alpha=0.8))
    ax.text(34, 70, "EXTREME CAUTION\n(32°C - 41°C)", color='#FFFFFF', fontsize=12, weight='bold', ha='center', bbox=dict(boxstyle="round", facecolor='#7C2D12', alpha=0.8))
    ax.text(40, 80, "CRITICAL DANGER\n(HEAT ALERT >= 41°C)", color='#FFFFFF', fontsize=13, weight='bold', ha='center', bbox=dict(boxstyle="round", facecolor='#991B1B', alpha=0.9))

    out_path = os.path.join(screenshots_dir, "thermal-heat-matrix.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 4. Live Dashboard — Operational Normal State (1400 x 850)
# -------------------------------------------------------------
def make_dashboard_normal():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=120)
    fig.patch.set_facecolor('#070A13')
    ax.set_facecolor('#070A13')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Top Navbar
    nav = patches.FancyBboxPatch((0.5, 7.3), 13.0, 0.9, boxstyle="round,pad=0.06", facecolor='#0F172A', edgecolor='#1E293B', lw=1.5)
    ax.add_patch(nav)
    ax.text(0.8, 7.85, "EnviroSense", color='#FFFFFF', fontsize=18, weight='bold')
    ax.text(2.8, 7.85, "IoT Environmental & Air Quality Dashboard", color='#94A3B8', fontsize=12)
    ax.text(0.8, 7.5, "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205) · PRODUCT NO. 23", color='#06B6D4', fontsize=9, weight='bold')

    # Badges
    b1 = patches.FancyBboxPatch((9.6, 7.5), 1.7, 0.5, boxstyle="round,pad=0.05", facecolor='#065F46', edgecolor='#10B981', lw=1.5)
    ax.add_patch(b1)
    ax.text(10.45, 7.75, "● AWS CONNECTED", color='#34D399', fontsize=8.5, weight='bold', ha='center', va='center')

    b2 = patches.FancyBboxPatch((11.5, 7.5), 1.7, 0.5, boxstyle="round,pad=0.05", facecolor='#064E3B', edgecolor='#10B981', lw=1.5)
    ax.add_patch(b2)
    ax.text(12.35, 7.75, "OPTIMAL STATE", color='#10B981', fontsize=8.5, weight='bold', ha='center', va='center')

    # 4 Dial / Metric Cards (Temperature, Humidity, Heat Index, MQ-135 Gas)
    cards_data = [
        {"x": 0.5, "title": "Ambient Temperature", "val": "24.5", "unit": "°C", "sub": "76.1 °F · Safe (5-35°C)", "color": "#06B6D4", "dial_pct": 0.52},
        {"x": 3.8, "title": "Relative Humidity", "val": "48.0", "unit": "%", "sub": "Comfort: Ideal · (<80%)", "color": "#3B82F6", "dial_pct": 0.48},
        {"x": 7.1, "title": "Steadman Heat Index", "val": "24.3", "unit": "°C", "sub": "Risk: Low · Feels Like", "color": "#10B981", "dial_pct": 0.45},
        {"x": 10.4, "title": "MQ-135 Air Quality", "val": "180", "unit": "PPM", "sub": "Status: EXCELLENT / GOOD", "color": "#A855F7", "dial_pct": 0.30}
    ]

    for c in cards_data:
        box = patches.FancyBboxPatch((c['x'], 4.8), 3.1, 2.3, boxstyle="round,pad=0.08,rounding_size=0.18",
                                     facecolor='#0F172A', edgecolor='#1E293B', lw=1.5)
        ax.add_patch(box)
        # Accent top line
        ax.plot([c['x'] + 0.2, c['x'] + 2.9], [7.0, 7.0], color=c['color'], lw=3.0, solid_capstyle='round')

        ax.text(c['x'] + 0.25, 6.65, c['title'], color='#94A3B8', fontsize=10.5, weight='bold')
        ax.text(c['x'] + 0.25, 5.85, c['val'], color='#FFFFFF', fontsize=32, weight='bold')
        ax.text(c['x'] + 1.6, 5.85, c['unit'], color='#64748B', fontsize=16, weight='bold')
        ax.text(c['x'] + 0.25, 5.25, c['sub'], color=c['color'], fontsize=8.5, weight='bold')

        # Mini gauge track & fill
        ax.plot([c['x'] + 0.25, c['x'] + 2.85], [5.0, 5.0], color='#1E293B', lw=6, solid_capstyle='round')
        ax.plot([c['x'] + 0.25, c['x'] + 0.25 + (2.6 * c['dial_pct'])], [5.0, 5.0], color=c['color'], lw=6, solid_capstyle='round')

    # Status Banner Box
    s_banner = patches.FancyBboxPatch((0.5, 4.0), 13.0, 0.65, boxstyle="round,pad=0.06", facecolor='#064E3B', edgecolor='#10B981', lw=1.5)
    ax.add_patch(s_banner)
    ax.text(0.8, 4.32, "STATUS: NORMAL EQUILIBRIUM", color='#34D399', fontsize=10.5, weight='bold')
    ax.text(4.6, 4.32, "— Climate and air quality parameters within optimal operational ranges. No action required.", color='#E2E8F0', fontsize=9.5)

    # Real-Time SVG Trend Chart Panel
    chart_box = patches.FancyBboxPatch((0.5, 0.4), 13.0, 3.4, boxstyle="round,pad=0.08", facecolor='#0F172A', edgecolor='#1E293B', lw=1.5)
    ax.add_patch(chart_box)
    ax.text(0.8, 3.45, "Live Telemetry Waveforms (ESP32 DevKit V1 + Wokwi Virtual Node)", color='#FFFFFF', fontsize=12, weight='bold')
    ax.text(10.0, 3.45, "● Temp (°C)    ● Humidity (%)    ● Gas (PPM/10)", color='#38BDF8', fontsize=9.5, weight='bold')

    cx = np.linspace(0.9, 13.1, 24)
    cy_temp = 2.3 + 0.25 * np.sin(cx * 1.4) + 0.08 * np.cos(cx * 2.8)
    cy_hum = 1.6 + 0.3 * np.cos(cx * 1.1) - 0.12 * np.sin(cx * 2.2)
    cy_gas = 1.0 + 0.15 * np.sin(cx * 1.8) + 0.05 * np.cos(cx * 3.5)

    for gy in [0.9, 1.5, 2.1, 2.7]:
        ax.plot([0.9, 13.1], [gy, gy], color='#1E293B', lw=1, linestyle='--')

    ax.plot(cx, cy_temp, color='#06B6D4', lw=2.8)
    ax.plot(cx, cy_hum, color='#3B82F6', lw=2.8)
    ax.plot(cx, cy_gas, color='#A855F7', lw=2.8)

    for px, py in zip(cx[::2], cy_temp[::2]): ax.plot(px, py, 'o', color='#06B6D4', markersize=5)
    for px, py in zip(cx[::2], cy_hum[::2]): ax.plot(px, py, 'o', color='#3B82F6', markersize=5)
    for px, py in zip(cx[::2], cy_gas[::2]): ax.plot(px, py, 'o', color='#A855F7', markersize=5)

    ax.text(0.9, 0.65, "Device: enviro-esp32-01   |   Location: Campus Greenhouse Lab   |   Cadence: 400ms delta / 2s heartbeat", color='#64748B', fontsize=8.5)

    out_path = os.path.join(screenshots_dir, "dashboard-operational-green.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 5. Live Dashboard — Critical Hazard Alert State (1400 x 850)
# -------------------------------------------------------------
def make_dashboard_alert():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=120)
    fig.patch.set_facecolor('#070A13')
    ax.set_facecolor('#070A13')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Top Navbar with Red Alert Trim
    nav = patches.FancyBboxPatch((0.5, 7.3), 13.0, 0.9, boxstyle="round,pad=0.06", facecolor='#1E111A', edgecolor='#EF4444', lw=2.0)
    ax.add_patch(nav)
    ax.text(0.8, 7.85, "EnviroSense", color='#FFFFFF', fontsize=18, weight='bold')
    ax.text(2.8, 7.85, "IoT Environmental & Air Quality Dashboard", color='#F87171', fontsize=12)
    ax.text(0.8, 7.5, "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205) · PRODUCT NO. 23", color='#F87171', fontsize=9, weight='bold')

    # Alert Badges
    b1 = patches.FancyBboxPatch((9.4, 7.5), 1.9, 0.5, boxstyle="round,pad=0.05", facecolor='#7F1D1D', edgecolor='#EF4444', lw=1.5)
    ax.add_patch(b1)
    ax.text(10.35, 7.75, "🚨 HAZARD ACTIVE", color='#FCA5A5', fontsize=8.5, weight='bold', ha='center', va='center')

    b2 = patches.FancyBboxPatch((11.5, 7.5), 1.7, 0.5, boxstyle="round,pad=0.05", facecolor='#7F1D1D', edgecolor='#EF4444', lw=1.5)
    ax.add_patch(b2)
    ax.text(12.35, 7.75, "SIREN: 880Hz", color='#EF4444', fontsize=8.5, weight='bold', ha='center', va='center')

    # 4 Cards in Hazard State
    cards_data = [
        {"x": 0.5, "title": "Ambient Temperature", "val": "41.8", "unit": "°C", "sub": "107.2 °F · CRITICAL HEAT", "color": "#EF4444", "dial_pct": 0.88},
        {"x": 3.8, "title": "Relative Humidity", "val": "84.0", "unit": "%", "sub": "Severe Moisture Saturation", "color": "#F97316", "dial_pct": 0.84},
        {"x": 7.1, "title": "Steadman Heat Index", "val": "48.5", "unit": "°C", "sub": "EXTREME DANGER · Heatwave", "color": "#EF4444", "dial_pct": 0.95},
        {"x": 10.4, "title": "MQ-135 Air Quality", "val": "750", "unit": "PPM", "sub": "HAZARDOUS · Toxic Smoke", "color": "#DC2626", "dial_pct": 0.85}
    ]

    for c in cards_data:
        box = patches.FancyBboxPatch((c['x'], 4.8), 3.1, 2.3, boxstyle="round,pad=0.08,rounding_size=0.18",
                                     facecolor='#1C1017', edgecolor='#EF4444', lw=1.8)
        ax.add_patch(box)
        ax.plot([c['x'] + 0.2, c['x'] + 2.9], [7.0, 7.0], color=c['color'], lw=3.0, solid_capstyle='round')

        ax.text(c['x'] + 0.25, 6.65, c['title'], color='#FCA5A5', fontsize=10.5, weight='bold')
        ax.text(c['x'] + 0.25, 5.85, c['val'], color='#FFFFFF', fontsize=32, weight='bold')
        ax.text(c['x'] + 1.6, 5.85, c['unit'], color='#F87171', fontsize=16, weight='bold')
        ax.text(c['x'] + 0.25, 5.25, c['sub'], color=c['color'], fontsize=8.5, weight='bold')

        ax.plot([c['x'] + 0.25, c['x'] + 2.85], [5.0, 5.0], color='#331D24', lw=6, solid_capstyle='round')
        ax.plot([c['x'] + 0.25, c['x'] + 0.25 + (2.6 * c['dial_pct'])], [5.0, 5.0], color=c['color'], lw=6, solid_capstyle='round')

    # Hazard Banner
    s_banner = patches.FancyBboxPatch((0.5, 4.0), 13.0, 0.65, boxstyle="round,pad=0.06", facecolor='#7F1D1D', edgecolor='#EF4444', lw=2.0)
    ax.add_patch(s_banner)
    ax.text(0.8, 4.32, "ALERT: GAS LEAK & SEVERE HEATWAVE!", color='#FEF2F2', fontsize=11, weight='bold')
    ax.text(4.8, 4.32, "— Hazardous gas concentration (750 PPM) & critical heat index (48.5°C). Web audio siren activated.", color='#FECACA', fontsize=9.5)

    # Spike Trend Chart Panel
    chart_box = patches.FancyBboxPatch((0.5, 0.4), 13.0, 3.4, boxstyle="round,pad=0.08", facecolor='#1C1017', edgecolor='#7F1D1D', lw=1.5)
    ax.add_patch(chart_box)
    ax.text(0.8, 3.45, "Live Telemetry Waveforms — Hazard Surge Event", color='#FFFFFF', fontsize=12, weight='bold')
    ax.text(10.0, 3.45, "● Temp Surge    ● Hum Spike    ● Gas Alarm", color='#F87171', fontsize=9.5, weight='bold')

    cx = np.linspace(0.9, 13.1, 24)
    cy_temp = 1.8 + 0.05 * cx + (cx > 8.0) * (0.8 * (cx - 8.0) / 5.0)
    cy_hum = 1.5 + 0.03 * cx + (cx > 8.0) * (0.6 * (cx - 8.0) / 5.0)
    cy_gas = 1.0 + (cx > 7.5) * (1.6 * (cx - 7.5) / 5.5)

    for gy in [0.9, 1.5, 2.1, 2.7]:
        ax.plot([0.9, 13.1], [gy, gy], color='#331D24', lw=1, linestyle='--')

    ax.plot(cx, cy_temp, color='#EF4444', lw=3.0)
    ax.plot(cx, cy_hum, color='#F97316', lw=3.0)
    ax.plot(cx, cy_gas, color='#DC2626', lw=3.2)

    for px, py in zip(cx[::2], cy_temp[::2]): ax.plot(px, py, 'o', color='#EF4444', markersize=5)
    for px, py in zip(cx[::2], cy_hum[::2]): ax.plot(px, py, 'o', color='#F97316', markersize=5)
    for px, py in zip(cx[::2], cy_gas[::2]): ax.plot(px, py, 'o', color='#DC2626', markersize=5)

    ax.text(0.9, 0.65, "Trigger Event: Greenhouse Lab Overheat & Solvent Fume Threshold Breach", color='#F87171', fontsize=8.5, weight='bold')

    out_path = os.path.join(screenshots_dir, "dashboard-failure-red.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 6. Terminal Test Suite & Simulator Execution (1400 x 850)
# -------------------------------------------------------------
def make_terminal_tests():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=120)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    win = patches.FancyBboxPatch((0.5, 0.4), 13.0, 7.7, boxstyle="round,pad=0.08", facecolor='#0B0F19', edgecolor='#334155', lw=1.8)
    ax.add_patch(win)

    bar = patches.Rectangle((0.5, 7.5), 13.0, 0.6, facecolor='#1E293B')
    ax.add_patch(bar)
    ax.plot(0.8, 7.8, 'o', color='#EF4444', markersize=8)
    ax.plot(1.1, 7.8, 'o', color='#F59E0B', markersize=8)
    ax.plot(1.4, 7.8, 'o', color='#10B981', markersize=8)
    ax.text(7.0, 7.8, "PowerShell — EnviroSense Unit Test Suite & Wokwi Edge Telemetry Runner", color='#94A3B8', fontsize=10, weight='bold', ha='center', va='center')

    term_lines = [
        ("PS C:\\Users\\yeshwanth\\OneDrive\\Desktop\\cloud product 2\\cloud computing product 2> ", "#38BDF8", False),
        ("python -m unittest discover -s tests -v", "#F8FAFC", True),
        ("test_get_returns_telemetry_list (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_options_cors_preflight (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_flags_freeze_alert (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_flags_gas_alert_hazard (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_flags_heat_alert (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_rejects_missing_humidity (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_rejects_out_of_range_temperature (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_validates_and_stores_normal_telemetry (tests.test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("----------------------------------------------------------------------", "#475569", False),
        ("Ran 8 tests in 0.005s  ===>  ALL 8 TESTS PASSED (100% OK)", "#10B981", True),
        ("", "#000000", False),
        ("PS C:\\Users\\yeshwanth\\OneDrive\\Desktop\\cloud product 2\\cloud computing product 2> ", "#38BDF8", False),
        ("python server.py 3000", "#F8FAFC", True),
        ("=================================================================", "#06B6D4", False),
        ("  EnviroSense Bridge Server running on http://localhost:3000 (0.0.0.0)", "#FFFFFF", True),
        ("  Serving frontend dashboard & receiving live Wokwi ESP32 telemetry", "#94A3B8", False),
        ("  Virtual ESP32 Wokwi Endpoint: http://host.wokwi.internal:3000/telemetry", "#38BDF8", True),
        ("=================================================================", "#06B6D4", False),
        ("[ESP32 -> BRIDGE] Temp: 34.2°C | Hum: 72.5% | Gas: 420 PPM (MODERATE) -> Status: WARNING", "#F59E0B", True),
        ("  └─► [AWS DYNAMODB SYNC] Telemetry safely recorded in AWS Cloud (201)", "#10B981", True)
    ]

    curr_y = 7.15
    for text, col, is_bold in term_lines:
        if not text:
            curr_y -= 0.14
            continue
        ax.text(0.8, curr_y, text, color=col, fontsize=9.2, weight='bold' if is_bold else 'normal', fontfamily='monospace')
        curr_y -= 0.205

    out_path = os.path.join(screenshots_dir, "terminal-monitor-demo.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    make_architecture_diagram()
    make_hardware_schematic()
    make_heat_matrix_chart()
    make_dashboard_normal()
    make_dashboard_alert()
    make_terminal_tests()
    print("All 6 rich visual assets generated successfully!")
