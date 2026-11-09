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
        {"x": 0.7, "y": 1.1, "w": 3.3, "h": 6.4, "title": "TIER 1: EDGE INGESTION", "color": "#06B6D4"},
        {"x": 4.5, "y": 1.1, "w": 2.8, "h": 6.4, "title": "TIER 2: API GATEWAY", "color": "#F59E0B"},
        {"x": 7.8, "y": 1.1, "w": 3.6, "h": 6.4, "title": "TIER 3: SERVERLESS COMPUTE", "color": "#FF9900"},
        {"x": 11.9, "y": 1.1, "w": 3.4, "h": 6.4, "title": "TIER 4: STORAGE & DASHBOARD", "color": "#10B981"}
    ]

    for t in tiers:
        # Outer Card
        bg = patches.FancyBboxPatch((t['x'], t['y']), t['w'], t['h'],
                                    boxstyle="round,pad=0.1,rounding_size=0.28",
                                    facecolor='#10172A', edgecolor='#1E293B', lw=1.5)
        ax.add_patch(bg)
        # Top Accent Line
        top_bar = patches.Rectangle((t['x'] + 0.2, t['y'] + t['h'] - 0.08), t['w'] - 0.4, 0.06, facecolor=t['color'])
        ax.add_patch(top_bar)
        # Title
        ax.text(t['x'] + t['w']/2, t['y'] + t['h'] - 0.45, t['title'],
                ha='center', va='center', color=t['color'], fontsize=11, weight='bold')

    def add_card(x, y, w, h, title, lines, color, fill='#162038'):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.18",
                                      facecolor=fill, edgecolor=color, lw=1.2)
        ax.add_patch(card)
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', color='#FFFFFF', fontsize=11, weight='bold')
        for i, line in enumerate(lines):
            ax.text(x + 0.2, y + h - 0.72 - (i * 0.34), "• " + line, ha='left', va='center', color='#CBD5E1', fontsize=9.2)

    # Tier 1 Components
    add_card(1.0, 4.4, 2.7, 2.4, "ESP32 Sensor Station", [
        "DOIT ESP32 DevKit V1 (240MHz)",
        "DHT11 / DHT22 Digital Sensor",
        "SSD1306 0.96\" I2C OLED",
        "Wi-Fi HTTP Client (6s polling)"
    ], "#06B6D4")

    add_card(1.0, 1.6, 2.7, 2.5, "Python Edge Simulator", [
        "Zero-dependency Python CLI",
        "Diurnal thermodynamic sine model",
        "Modes: Normal, Heat, Freeze",
        "--dry-run and --once test flags"
    ], "#38BDF8")

    # Tier 2 Components
    add_card(4.7, 4.4, 2.4, 2.4, "Amazon API Gateway v2", [
        "Lightweight HTTP Protocol",
        "CORS Wildcard Allowed (*)",
        "POST /telemetry Ingestion",
        "GET /telemetry Query",
        "Sub-15ms Latency Routing"
    ], "#F59E0B")

    add_card(4.7, 1.6, 2.4, 2.5, "Security & Gateway Config", [
        "Auto-deploy stage: $default",
        "SSL / TLS 1.3 Encryption",
        "Optional x-api-key intake",
        "CORS Preflight (OPTIONS 204)"
    ], "#FBBF24")

    # Tier 3 Components
    add_card(8.1, 4.3, 3.0, 2.5, "AWS Lambda Function", [
        "Runtime: Python 3.12 (128 MB)",
        "Input sanitization (-40°C to 85°C)",
        "Steadman Heat Index Engine",
        "DynamoDBCrudPolicy IAM bind"
    ], "#FF9900")

    add_card(8.1, 1.6, 3.0, 2.4, "Automated Hazard Classifier", [
        "HEAT_ALERT: Temp or HI >= 40°C",
        "FREEZE_ALERT: Temp <= 5°C",
        "HIGH_HUMIDITY: Humidity >= 85%",
        "NORMAL: Climate equilibrium"
    ], "#F43F5E")

    # Tier 4 Components
    add_card(12.2, 4.4, 2.8, 2.4, "Amazon DynamoDB (NoSQL)", [
        "Table: envirosense-telemetry",
        "Partition Key: deviceId (String)",
        "Pay-Per-Request Capacity",
        "24-hr TTL: expiresAt attribute"
    ], "#3B82F6")

    add_card(12.2, 1.6, 2.8, 2.5, "Amazon S3 Static Website", [
        "Public Read Website Hosting",
        "HTML5 / CSS3 Glassmorphism",
        "Zero external CDN scripts",
        "Offline interactive Demo presets"
    ], "#10B981")

    # Connecting Arrows
    def draw_arrow(x1, y1, x2, y2, text, color='#94A3B8'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5, mutation_scale=18))
        if text:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.22
            ax.text(mx, my, text, ha='center', va='center', color=color, fontsize=8.5, weight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='#070A13', edgecolor=color, lw=1))

    draw_arrow(3.7, 5.6, 4.7, 5.6, "HTTP POST JSON", "#06B6D4")
    draw_arrow(3.7, 2.8, 4.7, 2.8, "HTTP POST JSON", "#38BDF8")
    draw_arrow(7.1, 5.6, 8.1, 5.6, "Proxy Event", "#F59E0B")
    draw_arrow(11.1, 5.6, 12.2, 5.6, "PutItem + TTL", "#FF9900")

    # S3 Polling dashed arrow
    ax.annotate('', xy=(7.1, 2.0), xytext=(12.2, 2.0),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, linestyle="dashed", mutation_scale=16))
    ax.text(9.65, 2.25, "GET /telemetry (6s client polling)", ha='center', va='center', color="#10B981", fontsize=8.5, weight='bold',
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

    ax.text(8, 8.4, "EnviroSense — ESP32 + DHT11 + OLED Hardware Wiring Schematic", 
            ha='center', va='center', color='#FFFFFF', fontsize=22, weight='bold')
    ax.text(8, 7.95, "DOIT ESP32 DEVKIT V1 · 0.96\" I2C OLED (SSD1306) · DHT11 TEMPERATURE & HUMIDITY SENSOR", 
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
    # Left: 3V3 (y=3.8), GND (y=2.8)
    ax.plot([5.8, 6.2], [3.8, 3.8], color='#EF4444', lw=5)
    ax.text(6.3, 3.8, "3V3 (Power Out)", color='#F8FAFC', fontsize=10, weight='bold', va='center')

    ax.plot([5.8, 6.2], [2.8, 2.8], color='#64748B', lw=5)
    ax.text(6.3, 2.8, "GND (Common)", color='#F8FAFC', fontsize=10, weight='bold', va='center')

    # Right: GPIO 4 (y=4.2), GPIO 21 (y=3.4), GPIO 22 (y=2.6)
    ax.plot([9.8, 10.2], [4.2, 4.2], color='#38BDF8', lw=5)
    ax.text(9.7, 4.2, "GPIO 4 (DHT Data)", color='#F8FAFC', fontsize=10, weight='bold', ha='right', va='center')

    ax.plot([9.8, 10.2], [3.4, 3.4], color='#10B981', lw=5)
    ax.text(9.7, 3.4, "GPIO 21 (I2C SDA)", color='#F8FAFC', fontsize=10, weight='bold', ha='right', va='center')

    ax.plot([9.8, 10.2], [2.6, 2.6], color='#F59E0B', lw=5)
    ax.text(9.7, 2.6, "GPIO 22 (I2C SCL)", color='#F8FAFC', fontsize=10, weight='bold', ha='right', va='center')

    # 2. DHT11 Sensor (Left side)
    dht = patches.FancyBboxPatch((1.0, 2.2), 3.0, 4.5,
                                boxstyle="round,pad=0.1,rounding_size=0.25",
                                facecolor='#0284C7', edgecolor='#38BDF8', lw=2.5)
    ax.add_patch(dht)
    ax.text(2.5, 6.0, "DHT11 SENSOR", ha='center', va='center', color='#FFFFFF', fontsize=15, weight='bold')
    ax.text(2.5, 5.6, "Digital Temp & Humidity", ha='center', va='center', color='#E0F2FE', fontsize=10)

    # Grille pattern on DHT11
    for gy in [5.0, 4.6, 4.2, 3.8, 3.4]:
        ax.plot([1.6, 3.4], [gy, gy], color='#0369A1', lw=4)

    ax.text(2.5, 2.7, "Pinout: VCC | DATA | GND", ha='center', va='center', color='#FFFFFF', fontsize=9.5, weight='bold')

    # 3. SSD1306 OLED (Right side)
    oled = patches.FancyBboxPatch((11.8, 2.0), 3.2, 4.8,
                                 boxstyle="round,pad=0.1,rounding_size=0.25",
                                 facecolor='#1E293B', edgecolor='#F59E0B', lw=2.5)
    ax.add_patch(oled)
    ax.text(13.4, 6.2, "SSD1306 OLED", ha='center', va='center', color='#FFFFFF', fontsize=14, weight='bold')
    ax.text(13.4, 5.85, "0.96\" I2C Monochrome", ha='center', va='center', color='#94A3B8', fontsize=9.5)

    # OLED Glass area
    screen = patches.Rectangle((12.2, 3.3), 2.4, 2.2, facecolor='#000000', edgecolor='#475569', lw=1.5)
    ax.add_patch(screen)
    ax.text(13.4, 4.9, "EnviroSense  WiFi:OK", ha='center', va='center', color='#F59E0B', fontsize=8, weight='bold')
    ax.text(13.4, 4.3, "Temp: 24.5 C", ha='center', va='center', color='#38BDF8', fontsize=9.5, weight='bold')
    ax.text(13.4, 3.8, "Hum:  48.0 %", ha='center', va='center', color='#34D399', fontsize=9.5, weight='bold')

    ax.text(13.4, 2.5, "Pinout: VCC | GND | SCL | SDA", ha='center', va='center', color='#CBD5E1', fontsize=9, weight='bold')

    # Color-coded Wires
    # 3.3V Power (Red)
    ax.annotate("", xy=(5.8, 3.8), xytext=(4.0, 3.2),
                arrowprops=dict(arrowstyle="-", color="#EF4444", lw=3, connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(4.7, 3.9, "3.3V Power Rail", color="#EF4444", fontsize=9, weight='bold')

    # DHT11 Data to GPIO 4 (Blue)
    ax.annotate("", xy=(10.2, 4.2), xytext=(4.0, 2.8),
                arrowprops=dict(arrowstyle="-", color="#38BDF8", lw=3, connectionstyle="arc3,rad=0.35"))
    ax.text(7.2, 1.15, "DHT11 DATA ────────> GPIO 4", color="#38BDF8", fontsize=9.5, weight='bold')

    # OLED SDA (Green)
    ax.annotate("", xy=(11.8, 2.8), xytext=(10.2, 3.4),
                arrowprops=dict(arrowstyle="-", color="#10B981", lw=3, connectionstyle="arc3,rad=-0.1"))
    ax.text(11.0, 3.45, "SDA ──> GPIO 21", color="#10B981", fontsize=9, weight='bold')

    # OLED SCL (Yellow)
    ax.annotate("", xy=(11.8, 3.1), xytext=(10.2, 2.6),
                arrowprops=dict(arrowstyle="-", color="#F59E0B", lw=3, connectionstyle="arc3,rad=-0.2"))
    ax.text(11.0, 2.3, "SCL ──> GPIO 22", color="#F59E0B", fontsize=9, weight='bold')

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

    # Convert to Fahrenheit for Steadman formula
    T_F = (T * 9.0 / 5.0) + 32.0
    HI_F = (
        -42.379 + (2.04901523 * T_F) + (10.14333127 * H)
        - (0.22475541 * T_F * H) - (0.00683783 * (T_F**2)) - (0.05481717 * (H**2))
        + (0.00122874 * (T_F**2) * H) + (0.00085282 * T_F * (H**2)) - (0.00000199 * (T_F**2) * (H**2))
    )
    HI_C = (HI_F - 32.0) * 5.0 / 9.0

    # Contour plot with thermal risk levels
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

    # Risk Labels Annotations
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
