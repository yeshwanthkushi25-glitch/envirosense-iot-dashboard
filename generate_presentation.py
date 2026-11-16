import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path, img_dir):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_COLOR = RGBColor(7, 10, 19)        # #070A13 Dark Navy
    CARD_BG = RGBColor(15, 23, 42)        # #0F172A Dark Slate
    CARD_BORDER = RGBColor(30, 41, 59)    # #1E293B Border
    CYAN = RGBColor(6, 182, 212)          # #06B6D4 Primary Accent
    LIGHT_CYAN = RGBColor(56, 189, 248)   # #38BDF8
    AMBER = RGBColor(245, 158, 11)        # #F59E0B Warning / Secondary
    EMERALD = RGBColor(16, 185, 129)      # #10B981 Success
    RED = RGBColor(239, 68, 68)           # #EF4444 Danger
    WHITE = RGBColor(255, 255, 255)       # Text Primary
    SLATE = RGBColor(148, 163, 184)       # Text Secondary
    MUTED = RGBColor(100, 116, 139)       # Subtitles

    def add_slide_base(header_tag, title_text):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background shape
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

        # Top Banner / Header
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = header_tag.upper()
        p0.font.name = "Calibri"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = CYAN

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.name = "Calibri"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.space_before = Pt(3)

        return slide

    def add_card(slide, x, y, w, h, border_color=CARD_BORDER, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_COLOR
    bg1.line.fill.background()

    # Center hero card
    add_card(s1, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), CYAN)

    tb = s1.shapes.add_textbox(Inches(1.6), Inches(1.3), Inches(10.133), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205) · PRODUCT NO. 23"
    p.font.name = "Calibri"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = CYAN

    p = tf.add_paragraph()
    p.text = "EnviroSense"
    p.font.name = "Calibri"; p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = WHITE
    p.space_before = Pt(8)

    p = tf.add_paragraph()
    p.text = "End-to-End Serverless IoT Climate & Air Quality Monitoring Platform"
    p.font.name = "Calibri"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = LIGHT_CYAN
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = (
        "DOIT ESP32 DevKit V1  ·  DHT22 Temperature & Humidity  ·  MQ-135 Hazardous Gas  ·  SSD1306 OLED\n"
        "Amazon API Gateway HTTP v2  ·  AWS Lambda Python 3.12  ·  Amazon DynamoDB (TTL)  ·  Amazon S3 Dashboard\n"
        "Wokwi Virtual Hardware Simulator in VS Code  ·  Automated Cloud Relay & Real-Time Waveforms"
    )
    p.font.name = "Calibri"; p.font.size = Pt(12); p.font.color.rgb = SLATE
    p.space_before = Pt(14)

    p = tf.add_paragraph()
    p.text = (
        "Team Members: M. Yeshwanth (2503A53005) & V. Laxmiprasad (2503A53006)\n"
        "Batch: 59   |   Environment: AWS Learner Lab (us-east-1)   |   GitHub: yeshwanthkushi25-glitch/envirosense-iot-dashboard"
    )
    p.font.name = "Calibri"; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = EMERALD
    p.space_before = Pt(20)

    # -------------------------------------------------------------
    # SLIDE 2: Executive Summary & The Problem Solved
    # -------------------------------------------------------------
    s2 = add_slide_base("Overview & Motivation", "Executive Summary: Why We Engineered EnviroSense")
    
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), AMBER)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "THE PROBLEM IN CAMPUS FACILITIES"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = AMBER
    p = tf.add_paragraph()
    p.text = (
        "• Critical Laboratory Assets: University agricultural greenhouses, biological tissue cultures, and data-center server racks require strict temperature, moisture, and air quality governance.\n\n"
        "• Invisible Chemical & Fire Hazards: Volatile organic compounds (VOCs), solvent fumes, and gas leaks go undetected until toxic concentration levels occur.\n\n"
        "• Ephemeral & Unrecorded Data: Traditional analog thermometers provide only localized, glanceable numbers that cannot be tracked over time, audited, or accessed remotely.\n\n"
        "• Latent Thermal Danger: High humidity impedes evaporative cooling, making the 'Apparent Heat Index' significantly more hazardous than the dry-bulb ambient temperature alone."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(10)

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), EMERALD)
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "THE ENVIROSENSE CLOUD SOLUTION"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "• Dual Ingestion Edge: Real DOIT ESP32 hardware node with DHT22 + MQ-135 sensors AND Wokwi virtual simulator in VS Code streaming live JSON over WiFi.\n\n"
        "• Sub-15ms Serverless Ingestion: Amazon API Gateway HTTP API v2 dispatches telemetry to AWS Lambda compute at sub-cent scale.\n\n"
        "• Automated Scientific Mathematics: Lambda dynamically computes the Rothfusz Steadman Heat Index ('Feels Like') and evaluates multi-tier alert thresholds.\n\n"
        "• Zero-Cost Lifecycle Storage: Amazon DynamoDB stores time-series metrics with 24-hr Time-to-Live (TTL) auto-pruning, preventing runaway storage costs.\n\n"
        "• Interactive S3 Glassmorphic UI: 4 radial dials, real-time SVG trend curves, and Web Audio siren alerts accessible publicly from any browser."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: System Architecture (Figure 1 Embedded)
    # -------------------------------------------------------------
    s3 = add_slide_base("System Design", "4-Tier Serverless Cloud & Edge Architecture")
    fig1_path = os.path.join(img_dir, "architecture-diagram.png")
    if os.path.exists(fig1_path):
        s3.shapes.add_picture(fig1_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.3))

    add_card(s3, Inches(9.0), Inches(1.5), Inches(3.5), Inches(5.3), CYAN)
    tb = s3.shapes.add_textbox(Inches(9.2), Inches(1.7), Inches(3.1), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "ARCHITECTURAL TIERS"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "1. Tier 1: Edge Sensing\n"
        "   ESP32 DevKit V1 node sampling DHT22 & MQ-135 every 2s, or Wokwi simulator in VS Code.\n\n"
        "2. Tier 2: Ingestion API\n"
        "   Amazon API Gateway (v2) with CORS preflight and low-latency payload proxying.\n\n"
        "3. Tier 3: Compute Engine\n"
        "   AWS Lambda (Python 3.12) computing Steadman Heat Index & gas categorization.\n\n"
        "4. Tier 4: Storage & UI\n"
        "   Amazon DynamoDB (24h TTL) and Amazon S3 static glassmorphic dashboard."
    )
    p.font.size = Pt(10.5); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 4: Hardware Schematic (Figure 2 Embedded)
    # -------------------------------------------------------------
    s4 = add_slide_base("Edge Layer", "ESP32 DevKit V1 + DHT22 + MQ-135 + OLED Hardware Pinout")
    fig2_path = os.path.join(img_dir, "hardware-schematic.png")
    if os.path.exists(fig2_path):
        s4.shapes.add_picture(fig2_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.3))

    add_card(s4, Inches(9.0), Inches(1.5), Inches(3.5), Inches(5.3), LIGHT_CYAN)
    tb = s4.shapes.add_textbox(Inches(9.2), Inches(1.7), Inches(3.1), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "CIRCUIT SPECIFICATIONS"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = LIGHT_CYAN
    p = tf.add_paragraph()
    p.text = (
        "• ESP32 DevKit V1:\n"
        "   Dual-Core Xtensa @ 240MHz with 2.4GHz 802.11 b/g/n Wi-Fi.\n\n"
        "• DHT22 Sensor (GPIO 4):\n"
        "   Precision digital temp (-40 to 80°C) and relative humidity (0 to 100%).\n\n"
        "• MQ-135 Sensor (GPIO 34):\n"
        "   Electrochemical sensor wired to ADC1_CH6 (safe to run alongside Wi-Fi!).\n\n"
        "• SSD1306 OLED (I2C 0x3C):\n"
        "   GPIO 21 (SDA) & GPIO 22 (SCL) displaying local real-time metrics."
    )
    p.font.size = Pt(10.5); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 5: Virtual ESP32 Hardware Simulation in VS Code
    # -------------------------------------------------------------
    s5 = add_slide_base("VS Code Simulation", "Virtual Hardware in VS Code via Wokwi Simulator")
    
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), RGBColor(192, 132, 252))
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "ZERO-HARDWARE VS CODE SIMULATION"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = RGBColor(192, 132, 252)
    p = tf.add_paragraph()
    p.text = (
        "• Wokwi for VS Code Integration:\n"
        "   Powered by wokwi.toml and diagram.json directly inside VS Code workspace.\n\n"
        "• Virtual Wi-Fi Networking (Wokwi-GUEST):\n"
        "   The simulated ESP32 boots in emulated silicon, executes Xtensa binary instructions, connects to virtual Wi-Fi, and sends outbound HTTPS requests.\n\n"
        "• Interactive Peripheral Sliders:\n"
        "   Developers drag temperature (-40 to 80°C), humidity (0 to 100%), and gas (50 to 1000 PPM) sliders directly on the virtual breadboard.\n\n"
        "• Sub-400ms Delta Change Detection:\n"
        "   Firmware instantly detects slider motion and dispatches telemetry immediately without waiting for heartbeat timers."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), CYAN)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "DUAL-TRANSMISSION & AWS CLOUD RELAY"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "• Route 1: Direct HTTPS Cloud Ingestion\n"
        "   ESP32 firmware uses WiFiClientSecure with TLS validation to send POST requests directly to AWS API Gateway endpoint:\n"
        "   https://etejnaemlc.execute-api.us-east-1.amazonaws.com/telemetry\n\n"
        "• Route 2: Local Bridge & Async AWS Relay\n"
        "   server.py acts as a local gateway at host.wokwi.internal:3000. When receiving telemetry, it updates local UI and asynchronously forwards packets to AWS DynamoDB.\n\n"
        "• Seamless Live Sync:\n"
        "   Moving a slider in VS Code Wokwi updates the virtual OLED, triggers AWS Lambda, persists in DynamoDB, and animates the public S3 website in real time!"
    )
    p.font.size = Pt(10.5); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: Steadman Heat Index Matrix (Figure 3 Embedded)
    # -------------------------------------------------------------
    s6 = add_slide_base("Scientific Modeling", "Steadman Heat Index & Atmospheric Risk Spectrum")
    fig3_path = os.path.join(img_dir, "thermal-heat-matrix.png")
    if os.path.exists(fig3_path):
        s6.shapes.add_picture(fig3_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.3))

    add_card(s6, Inches(9.0), Inches(1.5), Inches(3.5), Inches(5.3), AMBER)
    tb = s6.shapes.add_textbox(Inches(9.2), Inches(1.7), Inches(3.1), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "ROTHFUSZ REGRESSION"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = AMBER
    p = tf.add_paragraph()
    p.text = (
        "• Scientific Empirical Formula:\n"
        "   HI = -42.379 + 2.049·T + 10.143·RH - 0.224·T·RH - 0.0068·T² - 0.054·RH² + 0.0012·T²·RH + 0.00085·T·RH² - 1.99e-6·T²·RH²\n\n"
        "• Alert Classification Matrix:\n"
        "   • NORMAL: Equilibrium (<27°C)\n"
        "   • WARNING: Caution (35°C to 40°C)\n"
        "   • HEAT_ALERT: Danger (>=40°C HI)\n"
        "   • FREEZE_ALERT: Frost (<=5°C)\n"
        "   • HIGH_HUMIDITY: Mildew (>=80%)\n"
        "   • GAS_ALERT: Toxic (>=600 PPM)"
    )
    p.font.size = Pt(10); p.font.color.rgb = SLATE; p.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 7: Serverless Compute & Persistence (Lambda + DynamoDB)
    # -------------------------------------------------------------
    s7 = add_slide_base("Cloud Infrastructure", "Serverless Compute Engine & NoSQL Persistence")
    
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), RGBColor(255, 153, 0))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "AWS LAMBDA ENGINE (Python 3.12)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = RGBColor(255, 153, 0)
    p = tf.add_paragraph()
    p.text = (
        "• HTTP API Routing:\n"
        "   Handles POST /telemetry (ingest), GET /telemetry (query), and OPTIONS (CORS preflight).\n\n"
        "• Input Validation & Range Bounds:\n"
        "   Verifies temperature (-40 to 85°C), humidity (0 to 100%), and gas concentration (0 to 10000 PPM).\n\n"
        "• Decimal Precision Conversion:\n"
        "   Converts floating-point metrics into Python Decimal types required by Boto3 DynamoDB storage.\n\n"
        "• Learner Lab Compatibility:\n"
        "   Conditionally binds to arn:aws:iam::<account>:role/LabRole to bypass sandbox IAM role creation restrictions."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), EMERALD)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "AMAZON DYNAMODB (24-HR TTL)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "• Table Schema:\n"
        "   envirosense-telemetry keyed by deviceId (Partition Key: String) with Pay-Per-Request on-demand capacity.\n\n"
        "• Automated Lifecycle Pruning (TTL):\n"
        "   Each item receives an expiresAt UNIX timestamp (now + 86,400s). DynamoDB purges expired items automatically at $0.00 compute cost.\n\n"
        "• Structured Item Attributes:\n"
        "   Stores temperatureC, humidityPct, heatIndexC, gasPpm, gasRaw, airQuality, status, statusDetail, location, and recordedAt."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 8: Responsive S3 Glassmorphic Web Dashboard
    # -------------------------------------------------------------
    s8 = add_slide_base("User Interface", "Responsive S3 Static Web Dashboard & SVG Dials")
    
    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), CYAN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "GLASSMORPHIC UI ARCHITECTURE"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "• Pure Zero-CDN Architecture:\n"
        "   Constructed with pure semantic HTML5, CSS3 glassmorphism, and vanilla ES6+ JavaScript. Functions seamlessly in air-gapped laboratory networks.\n\n"
        "• 4 Circular SVG Radial Gauges:\n"
        "   Renders stroke-dasharray vector arcs calibrated to calibrated metric scales: Temperature (0-60°C), Humidity (0-100%), Heat Index (0-60°C), and Gas PPM (0-1000 PPM).\n\n"
        "• Web Audio API Siren Synthesizer:\n"
        "   Oscillator-driven acoustic alarms (880Hz / 440Hz dual tone) triggered during critical heatwaves and toxic gas hazard states."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), LIGHT_CYAN)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "SMART API DETECTOR & SCENARIOS"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = LIGHT_CYAN
    p = tf.add_paragraph()
    p.text = (
        "• Intelligent Host Auto-Detection:\n"
        "   When loaded from S3, the dashboard automatically binds to the live AWS API Gateway URL. When loaded locally, it defaults to the local Wokwi bridge.\n\n"
        "• 5 One-Click Scenario Presets:\n"
        "   1. Greenhouse Normal (24.5°C, 48% RH, 180 PPM)\n"
        "   2. Heatwave Surge (41.8°C, 84% RH, 220 PPM)\n"
        "   3. Cold Frost Drop (2.4°C, 32% RH, 150 PPM)\n"
        "   4. Tropical Rain (29.2°C, 92% RH, 190 PPM)\n"
        "   5. Toxic Gas Leak (750 PPM Hazardous)\n\n"
        "• Real-Time Polling:\n"
        "   Active 1-second cadence polling DynamoDB for instantaneous updates."
    )
    p.font.size = Pt(10.5); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 9: Operational Normal State (Figure 4 Embedded)
    # -------------------------------------------------------------
    s9 = add_slide_base("Live Verification", "Dashboard Operational State: Normal Facility Equilibrium")
    fig4_path = os.path.join(img_dir, "dashboard-operational-green.png")
    if os.path.exists(fig4_path):
        s9.shapes.add_picture(fig4_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.3))

    add_card(s9, Inches(9.0), Inches(1.5), Inches(3.5), Inches(5.3), EMERALD)
    tb = s9.shapes.add_textbox(Inches(9.2), Inches(1.7), Inches(3.1), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "EQUILIBRIUM TELEMETRY"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "• Operating Parameters:\n"
        "   • Temp: 24.5 °C (76.1 °F)\n"
        "   • Relative Humidity: 48.0 %\n"
        "   • Steadman Heat Index: 24.3 °C\n"
        "   • Air Quality: 180 PPM (GOOD)\n\n"
        "• Visual System Indicators:\n"
        "   • Status: OPTIMAL OK\n"
        "   • Ambient Green Glow\n"
        "   • Live Smooth Waveforms\n"
        "   • WiFi OK / AWS Connected\n\n"
        "• Facility Context:\n"
        "   Optimal conditions for plant germination and server rack longevity."
    )
    p.font.size = Pt(10.5); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 10: Critical Hazard Alert State (Figure 5 Embedded)
    # -------------------------------------------------------------
    s10 = add_slide_base("Hazard Detection", "Dashboard Critical Hazard State: Gas Leak & Heat Alert")
    fig5_path = os.path.join(img_dir, "dashboard-failure-red.png")
    if os.path.exists(fig5_path):
        s10.shapes.add_picture(fig5_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.3))

    add_card(s10, Inches(9.0), Inches(1.5), Inches(3.5), Inches(5.3), RED)
    tb = s10.shapes.add_textbox(Inches(9.2), Inches(1.7), Inches(3.1), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "HAZARD RESPONSE"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = RED
    p = tf.add_paragraph()
    p.text = (
        "• Extreme Hazard Metrics:\n"
        "   • Temp: 41.8 °C (Critical Heat)\n"
        "   • Relative Humidity: 84.0 %\n"
        "   • Heat Index: 48.5 °C (Danger)\n"
        "   • Gas Level: 750 PPM (Toxic)\n\n"
        "• Multi-Channel Alarm:\n"
        "   • Visual: Pulsing Red Alert\n"
        "   • Audio: 880Hz Synthesizer Siren\n"
        "   • OLED: ALERT: GAS LEAK!\n"
        "   • DynamoDB: GAS_ALERT flag\n\n"
        "• Instant Recovery:\n"
        "   Returns to green equilibrium once sensor readings fall below thresholds."
    )
    p.font.size = Pt(10.5); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 11: Unit Testing & Verification (Figure 6 Embedded)
    # -------------------------------------------------------------
    s11 = add_slide_base("Quality Assurance", "Automated Unit Test Suite & Edge Simulator Execution")
    fig6_path = os.path.join(img_dir, "terminal-monitor-demo.png")
    if os.path.exists(fig6_path):
        s11.shapes.add_picture(fig6_path, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.3))

    add_card(s11, Inches(9.0), Inches(1.5), Inches(3.5), Inches(5.3), EMERALD)
    tb = s11.shapes.add_textbox(Inches(9.2), Inches(1.7), Inches(3.1), Inches(4.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "8/8 UNIT TESTS PASS"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "• test_get_returns_telemetry_list [PASS]\n"
        "• test_options_cors_preflight [PASS]\n"
        "• test_post_flags_freeze_alert [PASS]\n"
        "• test_post_flags_gas_alert_hazard [PASS]\n"
        "• test_post_flags_heat_alert [PASS]\n"
        "• test_post_rejects_missing_humidity [PASS]\n"
        "• test_post_rejects_out_of_range_temp [PASS]\n"
        "• test_post_validates_and_stores [PASS]\n\n"
        "• Execution Speed: 0.005 seconds\n"
        "• Pass Rate: 100% Offline Verifiable"
    )
    p.font.size = Pt(10); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 12: Live AWS Deployment & Infrastructure Verification
    # -------------------------------------------------------------
    s12 = add_slide_base("Live Deployment", "Live Deployed AWS Infrastructure (Learner Lab us-east-1)")
    
    add_card(s12, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), CYAN)
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "PRODUCTION DEPLOYMENT SPECIFICATIONS"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "• CloudFormation Stack: envirosense (Status: CREATE_COMPLETE / UPDATE_COMPLETE)\n"
        "• AWS Region: us-east-1 (US East, N. Virginia)   |   AWS Account ID: 683495019184\n"
        "• Execution IAM Role: arn:aws:iam::683495019184:role/LabRole (Zero permission errors)\n\n"
        "LIVE ENDPOINTS & RESOURCES:\n"
        "• Public S3 Static Website:\n"
        "   http://envirosense-dashboard-683495019184.s3-website-us-east-1.amazonaws.com\n"
        "• Amazon API Gateway HTTP API v2 Base Ingestion URL:\n"
        "   https://etejnaemlc.execute-api.us-east-1.amazonaws.com/telemetry\n"
        "• Amazon DynamoDB Time-Series Table:\n"
        "   envirosense-telemetry (On-Demand billing, TTL enabled on 'expiresAt')\n"
        "• AWS Lambda Compute Function:\n"
        "   envirosense-handler (Python 3.12, 128 MB RAM, 10s timeout)\n"
        "• Amazon S3 Static Storage Bucket:\n"
        "   envirosense-dashboard-683495019184 (Public read bucket policy enabled)"
    )
    p.font.size = Pt(12); p.font.color.rgb = WHITE; p.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 13: AWS Cost & Free Tier Analysis
    # -------------------------------------------------------------
    s13 = add_slide_base("Economics & Scale", "Comprehensive AWS Cost & Free Tier Architecture Analysis")
    
    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), EMERALD)
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "AWS FREE TIER ALLOWANCES"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "• AWS Lambda Compute:\n"
        "   1,000,000 requests/month and 3,200,000 seconds of compute time FREE every month.\n\n"
        "• Amazon DynamoDB NoSQL:\n"
        "   25 GB of storage, 25 provisioned Write Capacity Units (WCU), and 25 Read Capacity Units (RCU) FREE.\n\n"
        "• Amazon S3 Static Hosting:\n"
        "   5 GB of standard object storage and 20,000 GET requests FREE.\n\n"
        "• Amazon CloudWatch Logs:\n"
        "   5 GB of log data ingestion and archiving FREE."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), CYAN)
    tb = s13.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "ENVIROSENSE MONTHLY USAGE BILL"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "• 1 IoT Sensor Station (sampling every 5s):\n"
        "   518,400 invocations / month (well within the 1M free tier quota).\n\n"
        "• Lambda Compute Cost:\n"
        "   518,400 reqs × 0.015s × 128MB = $0.00.\n\n"
        "• DynamoDB Storage Cost:\n"
        "   24-hr TTL keeps active dataset under 15 MB. Monthly cost: $0.00.\n\n"
        "• S3 Frontend Storage Cost:\n"
        "   Total assets size = ~60 KB. Monthly cost: $0.00.\n\n"
        "• TOTAL MONTHLY EXPENDITURE = $0.00 (Zero idle cost!)"
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 14: Challenges & Engineering Solutions
    # -------------------------------------------------------------
    s14 = add_slide_base("Engineering Problem Solving", "Key Challenges Encountered & Technical Resolutions")
    
    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), AMBER)
    tb = s14.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "TECHNICAL CHALLENGES"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = AMBER
    p = tf.add_paragraph()
    p.text = (
        "1. AWS Learner Lab IAM Sandbox:\n"
        "   Sandbox forbids creating IAM roles, failing standard SAM/CloudFormation stacks.\n\n"
        "2. Hardware Dependency in Exam Halls:\n"
        "   Physical breadboards cannot always be connected to lecture hall Wi-Fi.\n\n"
        "3. DynamoDB Float Type Incompatibility:\n"
        "   Boto3 rejects Python floats, returning HTTP 400 Bad Request.\n\n"
        "4. High-Frequency Telemetry Accumulation:\n"
        "   Continuous sensor streams create 43,000+ items daily, threatening storage limits."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), EMERALD)
    tb = s14.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "ENGINEERED RESOLUTIONS"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "1. Parameterized 'UseLabRole: true':\n"
        "   Conditionally attaches existing LabRole (arn:aws:iam::<account>:role/LabRole).\n\n"
        "2. Wokwi Virtual Node & Built-In Demo Engine:\n"
        "   Runs full ESP32 simulation in VS Code + offline browser scenario presets.\n\n"
        "3. Decimal Type Serialization:\n"
        "   Sanitizes floats to Decimal(str(val)) for DynamoDB and provides JSON fallback.\n\n"
        "4. Native DynamoDB 24-hr TTL:\n"
        "   Automated background pruning expires items after 86,400s at zero compute cost."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 15: Step-by-Step Live Demo Walkthrough
    # -------------------------------------------------------------
    s15 = add_slide_base("Demonstration Guide", "Step-by-Step Live Demonstration Walkthrough")
    
    add_card(s15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), CYAN)
    tb = s15.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "DEMO SEQUENCE 1: VS CODE WOKWI"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "Step 1: Open diagram.json in VS Code.\n\n"
        "Step 2: Press F1 -> 'Wokwi: Start Simulator' (or click green Play button).\n\n"
        "Step 3: Observe virtual ESP32 connecting to Wokwi-GUEST and SSD1306 OLED displaying real-time metrics.\n\n"
        "Step 4: Click DHT22 to adjust Temperature (e.g. 42°C) or Humidity slider.\n\n"
        "Step 5: Click MQ-135 to adjust Gas Concentration (e.g. 700 PPM).\n\n"
        "Step 6: Confirm OLED and terminal log reflect changes within 400ms."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s15, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), LIGHT_CYAN)
    tb = s15.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "DEMO SEQUENCE 2: S3 WEB DASHBOARD"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = LIGHT_CYAN
    p = tf.add_paragraph()
    p.text = (
        "Step 1: Open public S3 website in browser:\n"
        "   http://envirosense-dashboard-683495019184.s3-website-us-east-1.amazonaws.com\n\n"
        "Step 2: Observe live AWS DynamoDB polling updating 4 circular radial gauges.\n\n"
        "Step 3: Test one-click scenario presets (Greenhouse, Heatwave, Cold Frost, Tropical Rain, Gas Leak Hazard).\n\n"
        "Step 4: Verify acoustic siren synthesis triggers on hazard states.\n\n"
        "Step 5: Run unit tests offline: python -m unittest discover -s tests (8/8 PASS)."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 16: Conclusion & Team Responsibilities
    # -------------------------------------------------------------
    s16 = add_slide_base("Conclusion", "Team Responsibilities & Academic Deliverables Summary")
    
    add_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), CYAN)
    tb = s16.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "M. YESHWANTH (2503A53005)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = CYAN
    p = tf.add_paragraph()
    p.text = (
        "• ESP32 C++ Firmware Development:\n"
        "   Wired DHT22 + MQ-135 + SSD1306 OLED in PlatformIO with fast 400ms delta change detection.\n\n"
        "• Virtual Circuit Engineering:\n"
        "   Authored diagram.json and wokwi.toml for seamless VS Code simulation.\n\n"
        "• AWS Infrastructure & Cloud Deployment:\n"
        "   Configured CloudFormation stack in us-east-1 and synchronized S3 static website.\n\n"
        "• Edge Simulator & Repository Management:\n"
        "   Built cross-platform Python CLI simulator and managed Git version control."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    add_card(s16, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), EMERALD)
    tb = s16.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "V. LAXMIPRASAD (2503A53006)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = EMERALD
    p = tf.add_paragraph()
    p.text = (
        "• AWS Lambda Compute Engine:\n"
        "   Engineered Python 3.12 handler, Steadman Heat Index engine, and gas hazard evaluator.\n\n"
        "• DynamoDB Lifecycle Design:\n"
        "   Implemented NoSQL schema, Boto3 Decimal serialization, and 24-hr TTL auto-pruning.\n\n"
        "• S3 Glassmorphic Web Dashboard:\n"
        "   Designed 4 circular SVG dials, Web Audio synthesizer, and dark glassmorphism.\n\n"
        "• Automated Quality Assurance:\n"
        "   Authored 8-case automated unit test suite with 100% pass verification."
    )
    p.font.size = Pt(11); p.font.color.rgb = SLATE; p.space_before = Pt(8)

    # Save presentation
    prs.save(output_path)
    print(f"Master Presentation remade successfully: {output_path}")

if __name__ == "__main__":
    base_dir = r"c:\Users\yeshwanth\OneDrive\Desktop\cloud product 2\cloud computing product 2"
    out_file = os.path.join(base_dir, "EnviroSense_Master_Presentation.pptx")
    img_dir = os.path.join(base_dir, "docs", "screenshots")
    create_deck(out_file, img_dir)
