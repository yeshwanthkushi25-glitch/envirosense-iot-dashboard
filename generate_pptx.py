import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_master_deck(output_path, img_dir):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Premium Color Palette
    BG_COLOR = RGBColor(10, 15, 29)         # #0A0F1D Obsidian Slate
    CARD_BG = RGBColor(18, 26, 47)          # #121A2F Frosted Slate
    CARD_BORDER = RGBColor(30, 45, 77)      # #1E2D4D Clean border
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8
    TEXT_BODY = RGBColor(226, 232, 240)     # #E2E8F0
    ACCENT_CYAN = RGBColor(6, 182, 212)     # #06B6D4 Electric Cyan
    ACCENT_EMERALD = RGBColor(16, 185, 129) # #10B981 Lush Green
    ACCENT_AMBER = RGBColor(245, 158, 11)   # #F59E0B Warm Amber
    ACCENT_CORAL = RGBColor(244, 63, 94)    # #F43F5E Alert Coral
    ACCENT_BLUE = RGBColor(59, 130, 246)    # #3B82F6 Sapphire

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()

    def add_header(slide, subtitle, title):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = subtitle.upper()
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(21)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, items, title_color=ACCENT_CYAN, pill_bg=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)

        # Top accent bar on card
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.1), top + Inches(0.08), width - Inches(0.2), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = title_color
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), width - Inches(0.5), height - Inches(0.45))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(10)

        for item in items:
            p = tf.add_paragraph()
            p.text = ("• " if not item.startswith("  ") else "   ") + item.strip()
            p.font.name = "Segoe UI"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_BODY
            p.space_after = Pt(5)

    def add_image_card(slide, left, top, width, height, image_path, caption=None):
        frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        frame.fill.solid()
        frame.fill.fore_color.rgb = CARD_BG
        frame.line.color.rgb = CARD_BORDER
        frame.line.width = Pt(1.2)

        # Insert picture inside frame
        pad = Inches(0.15)
        caption_space = Inches(0.4) if caption else Inches(0)
        img_w = width - (pad * 2)
        img_h = height - (pad * 2) - caption_space
        slide.shapes.add_picture(image_path, left + pad, top + pad, img_w, img_h)

        if caption:
            tb = slide.shapes.add_textbox(left + pad, top + height - caption_space, img_w, caption_space)
            tf = tb.text_frame
            p = tf.paragraphs[0]
            p.text = caption
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN

    # ---------------- SLIDE 1: Title Slide ----------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    
    # Background decorative glow
    glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1), Inches(11.733), Inches(5.3))
    glow.fill.solid()
    glow.fill.fore_color.rgb = CARD_BG
    glow.line.color.rgb = CARD_BORDER
    glow.line.width = Pt(1.5)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1), Inches(11.733), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_CYAN
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205)"
    p.font.name = "Segoe UI"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ACCENT_CYAN; p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "EnviroSense — IoT Climate & Environmental Dashboard"
    p.font.name = "Segoe UI"; p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = TEXT_WHITE; p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Serverless Environmental Telemetry, Steadman Heat Index Engine & S3 Static Monitoring"
    p.font.name = "Segoe UI"; p.font.size = Pt(15); p.font.color.rgb = TEXT_MUTED; p.space_after = Pt(24)

    p = tf.add_paragraph()
    p.text = "Project No.: 23    |    Batch: 59    |    Environment: AWS Learner Lab (us-east-1)"
    p.font.name = "Segoe UI"; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = ACCENT_AMBER; p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "Team Members:"
    p.font.name = "Segoe UI"; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = TEXT_WHITE; p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = "• M. Yeshwanth (H.T. No: 2503A53005) — ESP32 Firmware, Hardware Circuit & Python Edge Simulator\n• V. Laxmiprasad (H.T. No: 2503A53006) — AWS Serverless Backend, DynamoDB TTL & S3 Static Dashboard"
    p.font.name = "Segoe UI"; p.font.size = Pt(11.5); p.font.color.rgb = TEXT_BODY; p.space_after = Pt(18)

    p = tf.add_paragraph()
    p.text = "GitHub Repository: https://github.com/yeshwanthkushi25-glitch/envirosense-iot-dashboard"
    p.font.name = "Segoe UI"; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = ACCENT_CYAN

    # ---------------- SLIDE 2: Executive Summary ----------------
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Executive Summary & Why We Built EnviroSense")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "The Environmental Monitoring Challenge", [
        "Critical University Facilities: Agricultural greenhouses, biology labs, and server rooms demand tight climate equilibrium.",
        "Manual Spot-Checking: Analog wall thermometers are checked infrequently and results are unrecorded.",
        "Ephemeral Local Data: Standalone thermometers do not store historical telemetry for analytics or audits.",
        "Invisible Microclimates: Localized hot-spots or condensation spikes develop silently.",
        "Delayed Hazard Responses: Severe heatwaves or freezing conditions are discovered only after specimens or electronics are ruined."
    ], ACCENT_CORAL)
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "The EnviroSense Serverless Solution", [
        "Automated Edge-to-Cloud Telemetry: Continual wireless streaming from sensor nodes to AWS Cloud.",
        "Dual Ingestion Flexibility: Production ESP32 (DHT11+OLED) firmware and cross-platform Python CLI simulator.",
        "Serverless Apparent Temperature: AWS Lambda calculates the Steadman Heat Index ('Feels Like') server-side.",
        "Real-Time Hazard Alerting: Automated classification into NORMAL, HEAT_ALERT, FREEZE_ALERT, and HIGH_HUMIDITY.",
        "Zero-Cost Automated Pruning: DynamoDB TTL purges stale telemetry after 24 hours (100% Free Tier).",
        "S3 Glassmorphic Dashboard: Responsive web visualization with built-in 100% offline Demo Mode."
    ], ACCENT_EMERALD)

    # ---------------- SLIDE 3: System Architecture (WITH PICTURE!) ----------------
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "System Architecture & 4-Tier Serverless Data Flow")
    arch_img = os.path.join(img_dir, "architecture-diagram.png")
    add_image_card(s3, Inches(0.8), Inches(1.7), Inches(7.6), Inches(5.2), arch_img, "Figure 1: EnviroSense 4-Tier Serverless Cloud Architecture Diagram")
    add_card(s3, Inches(8.7), Inches(1.7), Inches(3.8), Inches(5.2), "Key Architectural Highlights", [
        "Tier 1: Edge Sensing",
        "  ESP32 node or Python simulator streams JSON payload every 5-6s.",
        "Tier 2: API Gateway v2",
        "  HTTP protocol with CORS preflight (*), providing <15ms ingestion latency.",
        "Tier 3: AWS Lambda",
        "  Python 3.12 sanitizes data, computes Steadman Heat Index, and flags alert states.",
        "Tier 4: Storage & UI",
        "  DynamoDB persists time-series records with 24h TTL; S3 serves the live dashboard."
    ], ACCENT_AMBER)

    # ---------------- SLIDE 4: Hardware Schematic (WITH PICTURE!) ----------------
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Microcontroller & Sensor Hardware Ingestion")
    schem_img = os.path.join(img_dir, "hardware-schematic.png")
    add_image_card(s4, Inches(0.8), Inches(1.7), Inches(7.4), Inches(5.2), schem_img, "Figure 2: ESP32 DevKit V1 + DHT11 Sensor + SSD1306 OLED Wiring Schematic")
    add_card(s4, Inches(8.5), Inches(1.7), Inches(4.0), Inches(5.2), "Hardware Engineering Features", [
        "ESP32 Microcontroller:",
        "  Dual-core 240MHz with 2.4GHz Wi-Fi.",
        "DHT11 Sensor:",
        "  Data connected to GPIO 4 (3.3V rail).",
        "SSD1306 0.96\" I2C OLED:",
        "  SDA -> GPIO 21, SCL -> GPIO 22.",
        "Local Status Readout:",
        "  Renders live Temp, Hum, Heat Index, and Wi-Fi signal on-board.",
        "Wi-Fi Auto-Reconnect:",
        "  Non-blocking background loop recovers gracefully if network drops."
    ], ACCENT_CYAN)

    # ---------------- SLIDE 5: Python Edge Simulator & Heat Matrix (WITH PICTURE!) ----------------
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Apparent Heat Index & Thermal Risk Spectrum")
    heat_img = os.path.join(img_dir, "thermal-heat-matrix.png")
    add_image_card(s5, Inches(0.8), Inches(1.7), Inches(7.4), Inches(5.2), heat_img, "Figure 3: NOAA / Steadman Heat Index Risk Matrix Calculation Spectrum")
    add_card(s5, Inches(8.5), Inches(1.7), Inches(4.0), Inches(5.2), "Steadman Risk Calculation", [
        "Serverless Computation:",
        "  Calculated dynamically in Python 3.12 Lambda using Rothfusz regression.",
        "Thermal Risk Bands:",
        "  • Normal / Safe: < 27°C (Emerald)",
        "  • Caution: 27°C - 32°C (Amber)",
        "  • Extreme Caution: 32°C - 41°C",
        "  • Critical Hazard: >= 41°C (Red)",
        "Automated Triggers:",
        "  Escalates to HEAT ALERT if temp or Heat Index exceeds 40°C."
    ], ACCENT_AMBER)

    # ---------------- SLIDE 6: Serverless Compute & Persistence ----------------
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Serverless Compute & Persistence (Lambda + DynamoDB)")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "AWS Lambda Ingestion Engine (Python 3.12)", [
        "HTTP API Routing: Handles POST /telemetry, GET /telemetry, and OPTIONS CORS preflight.",
        "Input Sanitization: Rejects out-of-bounds temperatures (-40°C to +85°C) and malformed payloads.",
        "Steadman Heat Index Engine: Implements NOAA/Rothfusz regression equation for apparent temperature.",
        "Automated Status Classification: Categorizes readings into NORMAL, HEAT_ALERT, FREEZE_ALERT, and HIGH_HUMIDITY.",
        "Stateless Auto-Scaling: Scales effortlessly from zero to thousands of simultaneous sensor nodes."
    ], ACCENT_CYAN)
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "Amazon DynamoDB with Automated TTL", [
        "NoSQL Schema: Partition Key 'deviceId' (String) stores current state and telemetry history.",
        "Pay-Per-Request Capacity: Zero idle cost; charges only per actual read/write operations.",
        "TTL Lifecycle (expiresAt): Automatically deletes records older than 24 hours without custom cron jobs.",
        "Sub-Millisecond Query Latency: Ensures instant real-time telemetry polling for the web dashboard.",
        "Learner Lab Optimization: Eliminates database bloat, keeping AWS credit spend strictly at $0.00."
    ], ACCENT_EMERALD)

    # ---------------- SLIDE 7: S3 Static Web Dashboard ----------------
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Responsive S3 Static Web Dashboard")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Modern Glassmorphic Architecture", [
        "Zero External CDN Dependencies: Pure vanilla HTML5, CSS3, and JavaScript.",
        "Air-Gapped & Offline Ready: Loads reliably inside classrooms, offline labs, or S3 public endpoints.",
        "Hero Telemetry Gauges: Large digital displays for Ambient Temp (°C & °F), Humidity (%), and Feels Like Heat Index.",
        "Color-Coded Progress Meters: Smoothly animated visual progress bars reflecting threshold percentages.",
        "Dark Theme UI: Tailored for 24/7 monitoring centers with glowing badges and high contrast."
    ], ACCENT_CYAN)
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "Real-Time SVG Chart & Dual Mode", [
        "Native SVG Trendline: Dynamically generates vector curves for the last 10 readings without external chart libraries.",
        "Dual Legend: Cyan line for Temperature (°C), Blue line for Humidity (%).",
        "Interactive Preset Buttons: One-click buttons to simulate Normal, Heatwave, Cold Wave, and High Humidity states.",
        "Continuous Auto-Stream: Generates realistic live ticks every 3 seconds for exhibition demos.",
        "Local Storage Memory: Retains API Gateway URLs and keys in browser memory across page reloads."
    ], ACCENT_AMBER)

    # ---------------- SLIDE 8: Demonstration: Normal (WITH PICTURE!) ----------------
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Demonstration: Normal Ambient Climate Monitoring")
    dash_norm_img = os.path.join(img_dir, "dashboard-operational-green.png")
    add_image_card(s8, Inches(0.8), Inches(1.7), Inches(7.4), Inches(5.2), dash_norm_img, "Figure 3: EnviroSense Dashboard — Operational Normal State (Glowing Green)")
    add_card(s8, Inches(8.5), Inches(1.7), Inches(4.0), Inches(5.2), "Normal State Evaluation", [
        "Facility Baseline Conditions:",
        "  Ambient Temp: 24.5 °C (76.1 °F).",
        "  Relative Humidity: 48.0 %.",
        "  Steadman Heat Index: 24.8 °C.",
        "Visual Indicators:",
        "  Header badge glows green 'NORMAL'.",
        "  Summary: 'All environmental metrics within safe operational thresholds.'",
        "Live SVG Waveform:",
        "  Renders smooth, balanced waves across the 10-sample observation window."
    ], ACCENT_EMERALD)

    # ---------------- SLIDE 9: Demonstration: Hazard Alerts (WITH PICTURE!) ----------------
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Demonstration: Critical Hazard Alerts & Recovery")
    dash_fail_img = os.path.join(img_dir, "dashboard-failure-red.png")
    add_image_card(s9, Inches(0.8), Inches(1.7), Inches(7.4), Inches(5.2), dash_fail_img, "Figure 4: EnviroSense Dashboard — Critical Thermal Hazard State (Pulsing Red Alert)")
    add_card(s9, Inches(8.5), Inches(1.7), Inches(4.0), Inches(5.2), "Hazard Alerting Logic", [
        "Critical Heatwave Event:",
        "  Trigger: 41.8 °C with 84.0 % Humidity.",
        "  Heat Index spikes to 94.6 °C.",
        "  System Badge: Pulsing 'HEAT ALERT'.",
        "  OLED Screen: 'ALERT: HEAT HAZARD!'.",
        "Cold Wave Event:",
        "  Trigger: 2.4 °C with 32.0 % Humidity.",
        "  System Badge: Shifts to 'FREEZE ALERT'.",
        "Instant Recovery:",
        "  Selecting 'Optimal (24°C)' immediately restores green NORMAL state."
    ], ACCENT_CORAL)

    # ---------------- SLIDE 10: Terminal Execution (WITH PICTURE!) ----------------
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Terminal Execution, Unit Testing & Verification")
    term_img = os.path.join(img_dir, "terminal-monitor-demo.png")
    add_image_card(s10, Inches(0.8), Inches(1.7), Inches(7.4), Inches(5.2), term_img, "Figure 5: Automated Unit Tests (100% Pass) & Edge Simulator Dry-Run Execution")
    add_card(s10, Inches(8.5), Inches(1.7), Inches(4.0), Inches(5.2), "Verification Suite Metrics", [
        "7 Automated Unit Tests:",
        "  • Valid Telemetry POST [PASS]",
        "  • Heatwave Hazard Alert [PASS]",
        "  • Freezing Alert Condition [PASS]",
        "  • Out-of-Bounds Rejection [PASS]",
        "  • Missing Attributes Rejection [PASS]",
        "  • GET /telemetry Retrieval [PASS]",
        "  • CORS Preflight OPTIONS [PASS]",
        "Execution Performance:",
        "  All 7 tests execute in 0.002s with mock DynamoDB — 100% pass rate."
    ], ACCENT_CYAN)

    # ---------------- SLIDE 11: Cost & Free Tier Analysis ----------------
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Comprehensive AWS Cost & Free Tier Analysis")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "AWS Free Tier Monthly Allowances", [
        "AWS Lambda: 1,000,000 requests/month & 3.2M seconds compute FREE.",
        "Amazon DynamoDB: 25 GB storage + 25 Write & Read Capacity Units FREE.",
        "Amazon S3: 5 GB Standard Storage + 20,000 GET requests FREE.",
        "Amazon API Gateway: 1,000,000 HTTP API calls/month FREE.",
        "AWS CloudWatch: 10 custom metrics + 5 GB log ingestion FREE."
    ], ACCENT_EMERALD)
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "EnviroSense Operational Monthly Usage", [
        "1 Sensor Node @ 6s interval = ~432,000 requests/month (within 1M free tier).",
        "Lambda Execution Time: Avg 15ms per call @ 128MB = ~6,480 GB-s (vastly below 400,000 GB-s).",
        "DynamoDB Storage with 24h TTL = ~14,400 active items (~4.3 MB total, << 25 GB).",
        "S3 Static Site: Static frontend footprint is <50 KB total.",
        "Net Monthly Cost in AWS Learner Lab: $0.00 (100% Free Tier Eligible)."
    ], ACCENT_AMBER)

    # ---------------- SLIDE 12: Limitations & Solutions 1 ----------------
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Project Limitations & Engineering Solutions — Part 1")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Limitation 1: Hardware Availability for Exam Demos", [
        "Challenge: Microcontrollers or lab breadboards may not be available during oral presentations.",
        "ENGINEERING SOLUTION:",
        "• Engineered a built-in browser-based Interactive Demo Engine inside the frontend.",
        "• Developed a cross-platform Python CLI simulator with multiple weather modes.",
        "• Students can demonstrate 100% of product features using just a standard laptop browser."
    ], ACCENT_CYAN)
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "Limitation 2: AWS Learner Lab Session Expirations", [
        "Challenge: Learner Lab credentials expire after 4 hours, causing API authentication dropouts.",
        "ENGINEERING SOLUTION:",
        "• Automated deployment script (deploy.ps1) with fast CloudFormation packaging.",
        "• Graceful dashboard fallback: Automatically shifts to Demo Mode if cloud API token expires.",
        "• LocalStorage saves API URLs so users don't need to re-type endpoints upon reconnection."
    ], ACCENT_AMBER)

    # ---------------- SLIDE 13: Limitations & Solutions 2 ----------------
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Project Limitations & Engineering Solutions — Part 2")
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Limitation 3: DynamoDB Storage Accumulation", [
        "Challenge: Continuous 6-second sensor pings generate 14,400 items per day per node.",
        "ENGINEERING SOLUTION:",
        "• Integrated native DynamoDB Time-To-Live (TTL) on attribute 'expiresAt'.",
        "• Items expire and purge automatically after 86,400 seconds (24 hours).",
        "• Eliminates maintenance overhead and guarantees zero storage bloat."
    ], ACCENT_CYAN)
    add_card(s13, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "Limitation 4: Learner Lab IAM Role Creation Block", [
        "Challenge: Learner Lab rejects IAM role creation requests in CloudFormation.",
        "ENGINEERING SOLUTION:",
        "• Codified cloudformation.yaml with 'UseLabRole: true' parameter.",
        "• Attaches pre-existing 'arn:aws:iam::<account>:role/LabRole' automatically.",
        "• SAM and CloudFormation deploy cleanly without permission denials."
    ], ACCENT_EMERALD)

    # ---------------- SLIDE 14: Academic Deliverables ----------------
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Academic Deliverables & Submission Package")
    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Document & Reporting Deliverables", [
        "1. Product Start Sheet: PRODUCT_START_SHEET.docx (Formal course sheet).",
        "2. Complete Product Report: PRODUCT_REPORT.docx (Full 6-section report).",
        "3. Hardware Wiring Schematic: wiring_schematic.md & hardware-schematic.png.",
        "4. Master README: README.md (Setup, architecture, tests & guides).",
        "5. Presentation Deck: EnviroSense_Master_Presentation.pptx (This 16-slide deck)."
    ], ACCENT_CYAN)
    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "Cloud, Code & Hardware Deliverables", [
        "6. AWS SAM Infrastructure: template.yaml & samconfig.toml.",
        "7. Pure CloudFormation: cloudformation.yaml (With Learner Lab LabRole).",
        "8. Microcontroller C++ Firmware: esp32_dht11_oled.ino.",
        "9. Python Edge Simulator: simulator/simulator.py.",
        "10. Automated Unit Test Suite: tests/test_lambda.py (100% pass).",
        "11. S3 Web Dashboard: frontend/ (index.html, styles.css, app.js).",
        "12. GitHub Repository: https://github.com/yeshwanthkushi25-glitch/envirosense-iot-dashboard."
    ], ACCENT_EMERALD)

    # ---------------- SLIDE 15: Step-by-Step Demo Walkthrough ----------------
    s15 = prs.slides.add_slide(blank_layout)
    set_bg(s15)
    add_header(s15, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Step-by-Step Live Demonstration Walkthrough")
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "Demo Sequence 1: Offline Browser Demo", [
        "1. Open frontend/index.html (or http://localhost:8080).",
        "2. Show initial baseline reading: 24.5 °C, 48% Humidity, NORMAL status.",
        "3. Click '🔥 Heatwave': Notice status turning pulsing RED ('HEAT ALERT').",
        "4. Point out the Steadman Heat Index escalating past 40°C danger zone.",
        "5. Click '❄️ Cold Wave': Notice status shifting to 'FREEZE ALERT'.",
        "6. Click '▶️ Start Live Stream': Watch the real-time SVG chart plot dynamic sensor curves every 3 seconds."
    ], ACCENT_AMBER)
    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "Demo Sequence 2: Edge Simulator & AWS Cloud", [
        "1. Open terminal and run: python simulator/simulator.py --dry-run --once.",
        "2. Show formatted JSON payload with deviceId, location, and computed heatIndex.",
        "3. Connect ESP32 hardware or run simulator with live API Gateway URL.",
        "4. Paste API Gateway URL into the dashboard and click 'Connect to AWS'.",
        "5. Badge shifts to 'AWS CONNECTED'; dashboard polls live DynamoDB records in real time.",
        "6. Show DynamoDB console displaying time-series records and TTL timestamps."
    ], ACCENT_CYAN)

    # ---------------- SLIDE 16: Conclusion & Team Contributions ----------------
    s16 = prs.slides.add_slide(blank_layout)
    set_bg(s16)
    add_header(s16, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Conclusion & Team Contributions")
    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), "M. Yeshwanth (H.T. No: 2503A53005)", [
        "• Researched course syllabus and selected Product #23 (IoT Environmental Dashboard).",
        "• Authored production ESP32 Arduino C++ firmware (esp32_dht11_oled.ino).",
        "• Designed complete hardware wiring schematic and I2C pinout documentation.",
        "• Developed Python edge sensor simulator (simulator.py) with atmospheric algorithms.",
        "• Validated multi-mode sensor streaming (Normal, Heatwave, Freeze, Fluctuate).",
        "• Configured Git repository, deployment scripts, and project packaging."
    ], ACCENT_CYAN)
    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.1), "V. Laxmiprasad (H.T. No: 2503A53006)", [
        "• Engineered AWS Lambda backend with Steadman Heat Index calculations (backend/app.py).",
        "• Codified CloudFormation (cloudformation.yaml) & SAM (template.yaml) with LabRole.",
        "• Configured Amazon DynamoDB with automated 24-hr TTL lifecycle management.",
        "• Developed S3 static glassmorphic dashboard with native SVG charting (frontend/).",
        "• Authored automated unit test suite (tests/test_lambda.py) achieving 100% pass rate.",
        "• Compiled academic documentation and master presentation deck."
    ], ACCENT_EMERALD)

    prs.save(output_path)
    print(f"Master Presentation with Embedded Graphics successfully generated at: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\yeshwanth\OneDrive\Desktop\cloud product 2\cloud computing product 2"
    img_dir = os.path.join(out_dir, "docs", "screenshots")
    create_master_deck(os.path.join(out_dir, "EnviroSense_Master_Presentation.pptx"), img_dir)
