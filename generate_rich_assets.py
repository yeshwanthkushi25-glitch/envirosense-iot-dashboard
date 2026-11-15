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

if __name__ == "__main__":
    make_architecture_diagram()
    make_hardware_schematic()
    make_heat_matrix_chart()
    print("All rich visual assets generated successfully!")
