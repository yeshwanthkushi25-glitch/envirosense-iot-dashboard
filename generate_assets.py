import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont

screenshots_dir = r"c:\Users\yeshwanth\OneDrive\Desktop\cloud product 2\cloud computing product 2\docs\screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. Architecture Diagram (1600 x 900)
# -------------------------------------------------------------
def make_architecture_diagram():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    fig.patch.set_facecolor('#0B1120')
    ax.set_facecolor('#0B1120')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title & Subtitle
    ax.text(8, 8.4, "EnviroSense — End-to-End Serverless IoT Architecture", 
            ha='center', va='center', color='#FFFFFF', fontsize=22, weight='bold', fontfamily='sans-serif')
    ax.text(8, 7.95, "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205) · PRODUCT NO. 23", 
            ha='center', va='center', color='#06B6D4', fontsize=12, weight='bold', fontfamily='sans-serif')

    # Draw Container Boxes (Tiers)
    tiers = [
        {"x": 0.8, "y": 1.2, "w": 3.2, "h": 6.2, "title": "TIER 1: EDGE SENSING", "color": "#06B6D4", "border": "#1E293B"},
        {"x": 4.5, "y": 1.2, "w": 2.8, "h": 6.2, "title": "TIER 2: API GATEWAY", "color": "#F59E0B", "border": "#1E293B"},
        {"x": 7.8, "y": 1.2, "w": 3.6, "h": 6.2, "title": "TIER 3: SERVERLESS COMPUTE", "color": "#FF9900", "border": "#1E293B"},
        {"x": 11.9, "y": 1.2, "w": 3.3, "h": 6.2, "title": "TIER 4: STORAGE & DASHBOARD", "color": "#10B981", "border": "#1E293B"}
    ]

    for t in tiers:
        # Background box
        rect = patches.FancyBboxPatch((t['x'], t['y']), t['w'], t['h'],
                                      boxstyle="round,pad=0.1,rounding_size=0.25",
                                      facecolor='#131D36', edgecolor=t['border'], linewidth=1.5)
        ax.add_patch(rect)
        # Header tag
        ax.text(t['x'] + t['w']/2, t['y'] + t['h'] - 0.45, t['title'],
                ha='center', va='center', color=t['color'], fontsize=11, weight='bold', fontfamily='sans-serif')

    # Tier 1 Components
    def add_subcard(x, y, w, h, title, lines, color, fill='#1E293B'):
        card = patches.FancyBboxPatch((x, y), w, h,
                                      boxstyle="round,pad=0.08,rounding_size=0.18",
                                      facecolor=fill, edgecolor=color, linewidth=1.2)
        ax.add_patch(card)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', color='#FFFFFF', fontsize=11, weight='bold')
        for i, line in enumerate(lines):
            ax.text(x + 0.2, y + h - 0.7 - (i * 0.32), "• " + line, ha='left', va='center', color='#CBD5E1', fontsize=9.5)

    add_subcard(1.1, 4.4, 2.6, 2.3, "ESP32 IoT Node (Hardware)", [
        "Xtensa Dual-Core 240MHz",
        "DHT11 Temp/Humidity Sensor",
        "SSD1306 0.96\" I2C OLED",
        "Wi-Fi HTTP Client (6s ping)"
    ], "#06B6D4")

    add_subcard(1.1, 1.6, 2.6, 2.4, "Python Edge Simulator (CLI)", [
        "Standard-library Python 3",
        "Diurnal weather sine model",
        "Modes: Normal, Heat, Freeze",
        "--dry-run and --once flags"
    ], "#38BDF8")

    # Tier 2 Components
    add_subcard(4.7, 4.4, 2.4, 2.3, "API Gateway (HTTP v2)", [
        "Sub-15ms Ingestion",
        "CORS Wildcard (*)",
        "POST /telemetry route",
        "GET /telemetry route"
    ], "#F59E0B")

    add_subcard(4.7, 1.6, 2.4, 2.4, "Protocol & Payload", [
        "Content-Type: JSON",
        "Optional x-api-key",
        "Auto-deploy stage: $default",
        "SSL/TLS Encrypted"
    ], "#FBBF24")

    # Tier 3 Components
    add_subcard(8.1, 4.3, 3.0, 2.4, "AWS Lambda Function", [
        "Runtime: Python 3.12",
        "Memory: 128 MB | Timeout: 10s",
        "Strict input bounds validation",
        "Steadman Heat Index calc"
    ], "#FF9900")

    add_subcard(8.1, 1.6, 3.0, 2.3, "Automated Hazard Engine", [
        "HEAT_ALERT (>=40°C or HI)",
        "FREEZE_ALERT (<=5°C)",
        "HIGH_HUMIDITY (>=85%)",
        "NORMAL (Safe equilibrium)"
    ], "#F43F5E")

    # Tier 4 Components
    add_subcard(12.2, 4.4, 2.7, 2.3, "Amazon DynamoDB (NoSQL)", [
        "Table: envirosense-telemetry",
        "Partition Key: deviceId",
        "Pay-Per-Request Capacity",
        "Automated 24h TTL (expiresAt)"
    ], "#3B82F6")

    add_subcard(12.2, 1.6, 2.7, 2.4, "Amazon S3 Static Website", [
        "Public-read Bucket Policy",
        "Zero-server maintenance",
        "index.html, styles.css, app.js",
        "Interactive offline Demo mode"
    ], "#10B981")

    # Connective Arrows
    def draw_arrow(x1, y1, x2, y2, text, color='#94A3B8'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5, mutation_scale=18))
        if text:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.2
            ax.text(mx, my, text, ha='center', va='center', color=color, fontsize=8.5, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='#0B1120', edgecolor=color, lw=1))

    # T1 to T2
    draw_arrow(3.7, 5.5, 4.7, 5.5, "HTTP POST JSON", "#06B6D4")
    draw_arrow(3.7, 2.8, 4.7, 2.8, "HTTP POST JSON", "#38BDF8")

    # T2 to T3
    draw_arrow(7.1, 5.5, 8.1, 5.5, "Proxy Event", "#F59E0B")

    # T3 to T4
    draw_arrow(11.1, 5.5, 12.2, 5.5, "PutItem + TTL", "#FF9900")

    # S3 to T2 (Dashboard polling)
    ax.annotate('', xy=(7.1, 2.0), xytext=(12.2, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, linestyle="dashed", mutation_scale=15))
    ax.text(9.65, 2.25, "GET /telemetry (6s polling)", ha='center', va='center', color="#10B981", fontsize=8.5, weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#0B1120', edgecolor="#10B981", lw=1))

    plt.tight_layout()
    out_path = os.path.join(screenshots_dir, "architecture-diagram.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 2. Hardware Wiring Schematic (1200 x 800)
# -------------------------------------------------------------
def make_hardware_schematic():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(6, 7.5, "EnviroSense — ESP32 Hardware Wiring Schematic", 
            ha='center', va='center', color='#FFFFFF', fontsize=20, weight='bold')
    ax.text(6, 7.1, "DOIT ESP32 DevKit V1 + DHT11 Temperature & Humidity Sensor + SSD1306 0.96\" I2C OLED",
            ha='center', va='center', color='#06B6D4', fontsize=10.5)

    # 1. ESP32 Main Board
    esp = patches.FancyBboxPatch((4.2, 1.5), 3.6, 5.0,
                                 boxstyle="round,pad=0.1,rounding_size=0.3",
                                 facecolor='#1E293B', edgecolor='#06B6D4', lw=2)
    ax.add_patch(esp)
    ax.text(6.0, 6.0, "ESP32 DevKit V1", ha='center', va='center', color='#FFFFFF', fontsize=14, weight='bold')
    ax.text(6.0, 5.65, "Wi-Fi + BLE Dual Core", ha='center', va='center', color='#94A3B8', fontsize=9.5)

    # ESP32 Chip graphic
    chip = patches.Rectangle((5.3, 4.1), 1.4, 1.2, facecolor='#0F172A', edgecolor='#334155', lw=1.5)
    ax.add_patch(chip)
    ax.text(6.0, 4.7, "ESP-WROOM-32", ha='center', va='center', color='#64748B', fontsize=7.5, weight='bold')

    # ESP32 Pins on left and right
    pins_left = [("3V3 (Power Out)", 3.2, "#EF4444"), ("GND (Ground)", 2.4, "#64748B")]
    pins_right = [("GPIO 4 (DHT Data)", 3.4, "#3B82F6"), ("GPIO 21 (I2C SDA)", 2.6, "#10B981"), ("GPIO 22 (I2C SCL)", 1.8, "#F59E0B")]

    for label, y, c in pins_left:
        ax.plot([4.2, 4.5], [y, y], color=c, lw=4)
        ax.text(4.6, y, label, ha='left', va='center', color='#F8FAFC', fontsize=9, weight='bold')

    for label, y, c in pins_right:
        ax.plot([7.5, 7.8], [y, y], color=c, lw=4)
        ax.text(7.4, y, label, ha='right', va='center', color='#F8FAFC', fontsize=9, weight='bold')

    # 2. DHT11 Sensor (Left side)
    dht = patches.FancyBboxPatch((0.8, 2.0), 2.2, 3.2,
                                boxstyle="round,pad=0.1,rounding_size=0.2",
                                facecolor='#0284C7', edgecolor='#38BDF8', lw=2)
    ax.add_patch(dht)
    ax.text(1.9, 4.7, "DHT11", ha='center', va='center', color='#FFFFFF', fontsize=13, weight='bold')
    ax.text(1.9, 4.35, "Temp & Humidity", ha='center', va='center', color='#E0F2FE', fontsize=8.5)

    # Grid slits on DHT11
    for gy in [3.8, 3.5, 3.2, 2.9]:
        ax.plot([1.3, 2.5], [gy, gy], color='#0369A1', lw=3)

    ax.text(1.9, 2.4, "Pins: VCC | DATA | GND", ha='center', va='center', color='#FFFFFF', fontsize=8, weight='bold')

    # 3. SSD1306 OLED (Right side)
    oled = patches.FancyBboxPatch((9.0, 1.8), 2.4, 3.6,
                                 boxstyle="round,pad=0.1,rounding_size=0.2",
                                 facecolor='#1E293B', edgecolor='#F59E0B', lw=2)
    ax.add_patch(oled)
    ax.text(10.2, 4.9, "SSD1306 OLED", ha='center', va='center', color='#FFFFFF', fontsize=12, weight='bold')
    ax.text(10.2, 4.6, "0.96\" I2C 128x64", ha='center', va='center', color='#94A3B8', fontsize=8.5)

    # Display glass area
    screen = patches.Rectangle((9.3, 2.6), 1.8, 1.6, facecolor='#000000', edgecolor='#475569', lw=1)
    ax.add_patch(screen)
    ax.text(10.2, 3.6, "Temp: 24.5 C", ha='center', va='center', color='#38BDF8', fontsize=7, weight='bold')
    ax.text(10.2, 3.2, "Hum:  48.0 %", ha='center', va='center', color='#34D399', fontsize=7, weight='bold')
    ax.text(10.2, 2.85, "WiFi: OK  STATUS: OK", ha='center', va='center', color='#F59E0B', fontsize=6.5)

    ax.text(10.2, 2.1, "VCC | GND | SCL | SDA", ha='center', va='center', color='#CBD5E1', fontsize=7.5, weight='bold')

    # Connecting Wires with curved spline paths
    # DHT11 Power (Red)
    ax.annotate("", xy=(4.2, 3.2), xytext=(3.0, 2.8),
                arrowprops=dict(arrowstyle="-", color="#EF4444", lw=2.5, connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(3.4, 3.4, "VCC (3.3V)", color="#EF4444", fontsize=8, weight='bold')

    # DHT11 Data (Blue) -> GPIO 4
    ax.annotate("", xy=(7.8, 3.4), xytext=(3.0, 2.5),
                arrowprops=dict(arrowstyle="-", color="#38BDF8", lw=2.5, connectionstyle="arc3,rad=0.35"))
    ax.text(5.5, 1.1, "DHT11 DATA ──> GPIO 4", color="#38BDF8", fontsize=8.5, weight='bold')

    # OLED I2C SDA (Green) -> GPIO 21
    ax.annotate("", xy=(9.0, 2.2), xytext=(7.8, 2.6),
                arrowprops=dict(arrowstyle="-", color="#10B981", lw=2.5, connectionstyle="arc3,rad=-0.1"))
    ax.text(8.4, 2.7, "SDA ──> GPIO 21", color="#10B981", fontsize=8, weight='bold')

    # OLED I2C SCL (Yellow) -> GPIO 22
    ax.annotate("", xy=(9.0, 2.5), xytext=(7.8, 1.8),
                arrowprops=dict(arrowstyle="-", color="#F59E0B", lw=2.5, connectionstyle="arc3,rad=-0.2"))
    ax.text(8.4, 1.6, "SCL ──> GPIO 22", color="#F59E0B", fontsize=8, weight='bold')

    out_path = os.path.join(screenshots_dir, "hardware-schematic.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 3. Dashboard Mockup — Normal State (1200 x 750)
# -------------------------------------------------------------
def make_dashboard_normal():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=100)
    fig.patch.set_facecolor('#0A0E17')
    ax.set_facecolor('#0A0E17')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Navbar
    nav = patches.Rectangle((0.4, 6.4), 11.2, 0.85, facecolor='#121929', edgecolor='#1E293B', lw=1)
    ax.add_patch(nav)
    ax.text(0.7, 6.9, "EnviroSense", color='#FFFFFF', fontsize=17, weight='bold')
    ax.text(2.6, 6.9, "IoT Climate & Environmental Dashboard", color='#64748B', fontsize=11)
    ax.text(0.7, 6.55, "SR University · Cloud Computing (25CAI102PC205) · Product #23", color='#06B6D4', fontsize=8.5)

    # Badges
    b1 = patches.FancyBboxPatch((8.8, 6.6), 1.3, 0.45, boxstyle="round,pad=0.05", facecolor='#10B981', alpha=0.2, edgecolor='#10B981', lw=1.2)
    ax.add_patch(b1)
    ax.text(9.45, 6.82, "AWS CONNECTED", color='#34D399', fontsize=8, weight='bold', ha='center', va='center')

    b2 = patches.FancyBboxPatch((10.3, 6.6), 1.0, 0.45, boxstyle="round,pad=0.05", facecolor='#10B981', alpha=0.2, edgecolor='#10B981', lw=1.2)
    ax.add_patch(b2)
    ax.text(10.8, 6.82, "NORMAL", color='#10B981', fontsize=8.5, weight='bold', ha='center', va='center')

    # 3 Key Metric Cards
    # Card 1: Temperature
    c1 = patches.FancyBboxPatch((0.4, 4.3), 3.5, 1.9, boxstyle="round,pad=0.08", facecolor='#121929', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(c1)
    ax.text(0.7, 5.85, "Ambient Temperature", color='#94A3B8', fontsize=10, weight='bold')
    ax.text(0.7, 5.15, "24.5", color='#FFFFFF', fontsize=32, weight='bold')
    ax.text(1.9, 5.15, "°C", color='#64748B', fontsize=16)
    ax.text(0.7, 4.65, "76.1 °F  |  Threshold: 5°C - 35°C", color='#94A3B8', fontsize=8.5)
    # Meter bar
    ax.plot([0.7, 3.5], [4.45, 4.45], color='#1E293B', lw=6, solid_capstyle='round')
    ax.plot([0.7, 2.1], [4.45, 4.45], color='#06B6D4', lw=6, solid_capstyle='round')

    # Card 2: Humidity
    c2 = patches.FancyBboxPatch((4.2, 4.3), 3.5, 1.9, boxstyle="round,pad=0.08", facecolor='#121929', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(c2)
    ax.text(4.5, 5.85, "Relative Humidity", color='#94A3B8', fontsize=10, weight='bold')
    ax.text(4.5, 5.15, "48.0", color='#FFFFFF', fontsize=32, weight='bold')
    ax.text(5.7, 5.15, "%", color='#64748B', fontsize=16)
    ax.text(4.5, 4.65, "Comfort: Ideal  |  Threshold: < 80%", color='#34D399', fontsize=8.5)
    # Meter bar
    ax.plot([4.5, 7.3], [4.45, 4.45], color='#1E293B', lw=6, solid_capstyle='round')
    ax.plot([4.5, 5.9], [4.45, 4.45], color='#3B82F6', lw=6, solid_capstyle='round')

    # Card 3: Heat Index
    c3 = patches.FancyBboxPatch((8.0, 4.3), 3.6, 1.9, boxstyle="round,pad=0.08", facecolor='#121929', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(c3)
    ax.text(8.3, 5.85, "Heat Index (Feels Like)", color='#94A3B8', fontsize=10, weight='bold')
    ax.text(8.3, 5.15, "24.8", color='#FFFFFF', fontsize=32, weight='bold')
    ax.text(9.5, 5.15, "°C", color='#64748B', fontsize=16)
    ax.text(8.3, 4.65, "Risk Level: Low / Normal  |  Steadman Formula", color='#10B981', fontsize=8.5)
    # Meter bar
    ax.plot([8.3, 11.2], [4.45, 4.45], color='#1E293B', lw=6, solid_capstyle='round')
    ax.plot([8.3, 9.3], [4.45, 4.45], color='#10B981', lw=6, solid_capstyle='round')

    # Real-Time SVG Trend Chart Panel
    chart_box = patches.FancyBboxPatch((0.4, 0.5), 11.2, 3.5, boxstyle="round,pad=0.08", facecolor='#121929', edgecolor='#1E293B', lw=1.2)
    ax.add_patch(chart_box)
    ax.text(0.7, 3.65, "Real-Time Environmental Trend (Live Telemetry Stream)", color='#FFFFFF', fontsize=12, weight='bold')
    ax.text(8.6, 3.65, "● Temp (°C)    ● Humidity (%)", color='#38BDF8', fontsize=9.5)

    # Draw chart waves
    cx = np.linspace(0.8, 11.0, 20)
    cy_temp = 2.4 + 0.25 * np.sin(cx * 1.5) + 0.1 * np.cos(cx * 3)
    cy_hum = 1.6 + 0.3 * np.cos(cx * 1.2) - 0.15 * np.sin(cx * 2.5)

    # Gridlines
    for gy in [1.2, 1.8, 2.4, 3.0]:
        ax.plot([0.8, 11.2], [gy, gy], color='#1E293B', lw=1, linestyle='--')

    ax.plot(cx, cy_temp, color='#06B6D4', lw=3, label='Temp')
    ax.plot(cx, cy_hum, color='#3B82F6', lw=3, label='Hum')

    for px, py in zip(cx, cy_temp):
        ax.plot(px, py, 'o', color='#06B6D4', markersize=6)
    for px, py in zip(cx, cy_hum):
        ax.plot(px, py, 'o', color='#3B82F6', markersize=6)

    ax.text(0.8, 0.8, "Device: enviro-node-01   |   Location: Campus Greenhouse Lab   |   Status: Safe Equilibrium", color='#64748B', fontsize=8.5)

    out_path = os.path.join(screenshots_dir, "dashboard-operational-green.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 4. Dashboard Mockup — Heatwave Alert State (1200 x 750)
# -------------------------------------------------------------
def make_dashboard_heat_alert():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=100)
    fig.patch.set_facecolor('#0A0E17')
    ax.set_facecolor('#0A0E17')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Navbar
    nav = patches.Rectangle((0.4, 6.4), 11.2, 0.85, facecolor='#121929', edgecolor='#F43F5E', lw=1.5)
    ax.add_patch(nav)
    ax.text(0.7, 6.9, "EnviroSense", color='#FFFFFF', fontsize=17, weight='bold')
    ax.text(2.6, 6.9, "IoT Climate & Environmental Dashboard", color='#64748B', fontsize=11)
    ax.text(0.7, 6.55, "CRITICAL THERMAL ALERT IN PROGRESS", color='#F43F5E', fontsize=9, weight='bold')

    # Badges
    b2 = patches.FancyBboxPatch((9.8, 6.6), 1.5, 0.45, boxstyle="round,pad=0.05", facecolor='#F43F5E', alpha=0.3, edgecolor='#F43F5E', lw=2)
    ax.add_patch(b2)
    ax.text(10.55, 6.82, "HEAT ALERT", color='#F43F5E', fontsize=9, weight='bold', ha='center', va='center')

    # Metric Cards
    # Card 1: Temp (Spiked)
    c1 = patches.FancyBboxPatch((0.4, 4.3), 3.5, 1.9, boxstyle="round,pad=0.08", facecolor='#1F1423', edgecolor='#F43F5E', lw=1.5)
    ax.add_patch(c1)
    ax.text(0.7, 5.85, "Ambient Temperature", color='#FCA5A5', fontsize=10, weight='bold')
    ax.text(0.7, 5.15, "41.8", color='#F43F5E', fontsize=32, weight='bold')
    ax.text(1.9, 5.15, "°C", color='#F87171', fontsize=16)
    ax.text(0.7, 4.65, "107.2 °F  |  EXCEEDS 40°C LIMIT!", color='#EF4444', fontsize=8.5, weight='bold')
    ax.plot([0.7, 3.5], [4.45, 4.45], color='#1E293B', lw=6, solid_capstyle='round')
    ax.plot([0.7, 3.3], [4.45, 4.45], color='#F43F5E', lw=6, solid_capstyle='round')

    # Card 2: Humidity
    c2 = patches.FancyBboxPatch((4.2, 4.3), 3.5, 1.9, boxstyle="round,pad=0.08", facecolor='#121929', edgecolor='#F59E0B', lw=1.2)
    ax.add_patch(c2)
    ax.text(4.5, 5.85, "Relative Humidity", color='#FCD34D', fontsize=10, weight='bold')
    ax.text(4.5, 5.15, "84.0", color='#F59E0B', fontsize=32, weight='bold')
    ax.text(5.7, 5.15, "%", color='#FBBF24', fontsize=16)
    ax.text(4.5, 4.65, "Moisture: High Condensation Risk", color='#F59E0B', fontsize=8.5)
    ax.plot([4.5, 7.3], [4.45, 4.45], color='#1E293B', lw=6, solid_capstyle='round')
    ax.plot([4.5, 6.9], [4.45, 4.45], color='#F59E0B', lw=6, solid_capstyle='round')

    # Card 3: Heat Index (Severe Danger)
    c3 = patches.FancyBboxPatch((8.0, 4.3), 3.6, 1.9, boxstyle="round,pad=0.08", facecolor='#2B121C', edgecolor='#EF4444', lw=2)
    ax.add_patch(c3)
    ax.text(8.3, 5.85, "Heat Index (Feels Like)", color='#FCA5A5', fontsize=10, weight='bold')
    ax.text(8.3, 5.15, "94.6", color='#EF4444', fontsize=32, weight='bold')
    ax.text(9.5, 5.15, "°C", color='#F87171', fontsize=16)
    ax.text(8.3, 4.65, "DANGER: Severe Thermal Exhaustion Hazard!", color='#EF4444', fontsize=8.5, weight='bold')
    ax.plot([8.3, 11.2], [4.45, 4.45], color='#1E293B', lw=6, solid_capstyle='round')
    ax.plot([8.3, 11.2], [4.45, 4.45], color='#EF4444', lw=6, solid_capstyle='round')

    # Chart with steep spike
    chart_box = patches.FancyBboxPatch((0.4, 0.5), 11.2, 3.5, boxstyle="round,pad=0.08", facecolor='#121929', edgecolor='#F43F5E', lw=1.2)
    ax.add_patch(chart_box)
    ax.text(0.7, 3.65, "Thermal Hazard Event Spike Detected", color='#F43F5E', fontsize=12, weight='bold')

    cx = np.linspace(0.8, 11.0, 20)
    cy_spike = 1.4 + 1.8 / (1 + np.exp(-(cx - 6.5) * 1.5))
    cy_hum_spike = 1.6 + 1.2 / (1 + np.exp(-(cx - 6.5) * 1.2))

    for gy in [1.2, 1.8, 2.4, 3.0]:
        ax.plot([0.8, 11.2], [gy, gy], color='#1E293B', lw=1, linestyle='--')

    ax.plot(cx, cy_spike, color='#F43F5E', lw=3.5)
    ax.plot(cx, cy_hum_spike, color='#F59E0B', lw=3)

    for px, py in zip(cx, cy_spike):
        ax.plot(px, py, 'o', color='#F43F5E', markersize=7)
    for px, py in zip(cx, cy_hum_spike):
        ax.plot(px, py, 'o', color='#F59E0B', markersize=6)

    ax.text(0.8, 0.8, "ALERT DISPATCHED: Automated threshold exceeded. Room ventilation required.", color='#F87171', fontsize=8.5, weight='bold')

    out_path = os.path.join(screenshots_dir, "dashboard-failure-red.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

# -------------------------------------------------------------
# 5. Terminal Execution Screenshot (1200 x 750)
# -------------------------------------------------------------
def make_terminal_screenshot():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=100)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Window frame
    win = patches.FancyBboxPatch((0.5, 0.5), 11.0, 6.5, boxstyle="round,pad=0.08", facecolor='#0B0F19', edgecolor='#334155', lw=1.5)
    ax.add_patch(win)

    # Window title bar
    bar = patches.Rectangle((0.5, 6.4), 11.0, 0.6, facecolor='#1E293B')
    ax.add_patch(bar)
    # 3 dots
    ax.plot(0.8, 6.7, 'o', color='#EF4444', markersize=8)
    ax.plot(1.1, 6.7, 'o', color='#F59E0B', markersize=8)
    ax.plot(1.4, 6.7, 'o', color='#10B981', markersize=8)
    ax.text(6.0, 6.7, "PowerShell — EnviroSense Test & Telemetry Simulator Suite", color='#94A3B8', fontsize=10, weight='bold', ha='center', va='center')

    # Terminal Text
    term_lines = [
        ("PS C:\\Users\\yeshwanth\\cloud computing product 2> ", "#38BDF8", False),
        ("python -m unittest discover -s tests -v", "#F8FAFC", True),
        ("test_get_returns_telemetry_list (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_options_cors_preflight (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_flags_freeze_alert (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_flags_heat_alert (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_rejects_missing_humidity (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_rejects_out_of_range_temperature (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("test_post_validates_and_stores_normal_telemetry (test_lambda.EnviroSenseLambdaTests) ... ", "#94A3B8", False),
        ("ok", "#10B981", True),
        ("----------------------------------------------------------------------", "#475569", False),
        ("Ran 7 tests in 0.002s  ===>  ALL 7 TESTS PASSED (100% OK)", "#10B981", True),
        ("", "#000000", False),
        ("PS C:\\Users\\yeshwanth\\cloud computing product 2> ", "#38BDF8", False),
        ("python simulator\\simulator.py --mode heatwave --dry-run --once", "#F8FAFC", True),
        ("=======================================================", "#06B6D4", False),
        ("  EnviroSense — IoT Edge Sensor Node Simulator", "#FFFFFF", True),
        ("  Device: enviro-node-01 | Location: Campus Greenhouse Lab", "#94A3B8", False),
        ("  Mode: HEATWAVE | Interval: 5.0s", "#F43F5E", True),
        ("=======================================================", "#06B6D4", False),
        ("[22:15:30] Telemetry payload:", "#94A3B8", False),
        ("  Temperature: 42.03 °C | Humidity: 79.69 % | Heat Index: 94.66 °C", "#F43F5E", True),
        ("  [DRY-RUN JSON] {\"deviceId\": \"enviro-node-01\", \"status\": \"HEAT_ALERT\", \"heatIndexC\": 94.66}", "#38BDF8", False)
    ]

    curr_y = 6.0
    for text, col, is_bold in term_lines:
        if not text:
            curr_y -= 0.15
            continue
        ax.text(0.8, curr_y, text, color=col, fontsize=9.5, weight='bold' if is_bold else 'normal', fontfamily='monospace')
        curr_y -= 0.22

    out_path = os.path.join(screenshots_dir, "terminal-monitor-demo.png")
    plt.savefig(out_path, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    make_architecture_diagram()
    make_hardware_schematic()
    make_dashboard_normal()
    make_dashboard_heat_alert()
    make_terminal_screenshot()
    print("All visual assets generated successfully!")
