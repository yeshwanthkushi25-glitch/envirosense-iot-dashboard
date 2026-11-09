import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]

    # Colors
    BG_COLOR = RGBColor(11, 17, 32)        # #0B1120 Deep Navy
    CARD_BG = RGBColor(19, 29, 54)         # #131D36 Slate Card
    BORDER_COLOR = RGBColor(30, 41, 59)    # #1E293B
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8
    TEXT_BODY = RGBColor(226, 232, 240)    # #E2E8F0
    ACCENT_CYAN = RGBColor(6, 182, 212)    # #06B6D4
    ACCENT_GREEN = RGBColor(16, 185, 129)  # #10B981
    ACCENT_AMBER = RGBColor(245, 158, 11)  # #F59E0B
    ACCENT_RED = RGBColor(244, 63, 94)     # #F43F5E

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background() # No border
        return bg

    def add_header(slide, subtitle, title):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = subtitle.upper()
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, items, title_color=ACCENT_CYAN):
        # Card Background box
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR
        box.line.width = Pt(1)

        # Text Frame
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), width - Inches(0.5), height - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Segoe UI"
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(12)
            first = False
        else:
            first = True

        for item in items:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = ("• " if not item.startswith("  ") else "   ") + item.strip()
            p.font.name = "Segoe UI"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_BODY
            p.space_after = Pt(6)

    # ================= SLIDE 1: Title Slide =================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1)
    
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "EnviroSense — IoT Climate & Environmental Dashboard"
    p.font.name = "Segoe UI"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "End-to-End Serverless Climate Telemetry, Heat Index Computation & S3 Static Monitoring"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(28)

    p = tf.add_paragraph()
    p.text = "Project No.: 23    |    Batch: 59    |    Environment: AWS Learner Lab (us-east-1)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "Team Members:"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = "• M. Yeshwanth (H.T. No: 2503A53005) — ESP32 Firmware, Edge Simulator & Hardware Schematics\n• V. Laxmiprasad (H.T. No: 2503A53006) — AWS Serverless Backend, DynamoDB TTL & S3 Static Dashboard"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_BODY
    p.space_after = Pt(16)

    p = tf.add_paragraph()
    p.text = "GitHub Repository: https://github.com/yeshwanthkushi25-glitch/envirosense-iot-dashboard"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN

    # ================= SLIDE 2: Executive Summary =================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2)
    add_header(s2, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Executive Summary & Why We Built EnviroSense")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "The Environmental Monitoring Challenge", [
        "Campus Laboratories & Greenhouses require constant temperature & humidity control.",
        "Manual Inspections: Spot-checking analogue wall thermometers is error-prone and unrecorded.",
        "Invisible Microclimates: Localized heat traps or moisture spikes ruin sensitive experiments.",
        "Ephemeral Local Data: Standalone sensors lack long-term historical records and analytics.",
        "Delayed Hazard Warnings: Extreme thermal spikes (heatwaves or freezing) remain unnoticed until equipment damages occur."
    ], ACCENT_RED)
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "The EnviroSense Serverless Solution", [
        "End-to-End IoT Telemetry: Continuous automated sensor streaming to AWS Cloud.",
        "Dual Ingestion Modes: Production ESP32 (DHT11+OLED) firmware + Python CLI simulator.",
        "Cloud-Native Serverless Processing: AWS HTTP API Gateway routes data to Python 3.12 Lambda.",
        "Algorithmic Risk Assessment: Computes Steadman Heat Index ('Feels Like') server-side.",
        "Automated NoSQL Retention: DynamoDB TTL purges stale items after 24 hrs for zero cost.",
        "Zero-Dependency S3 Dashboard: Fast, glassmorphic monitoring with 100% offline Demo Mode."
    ], ACCENT_GREEN)

    # ================= SLIDE 3: System Architecture =================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3)
    add_header(s3, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "System Architecture & 4-Tier Serverless Data Flow")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 1: Edge Ingestion", [
        "ESP32 Microcontroller",
        "DHT11 / DHT22 Sensor",
        "SSD1306 0.96\" I2C OLED",
        "Wi-Fi HTTP Client",
        "Python Edge Simulator (CLI)",
        "Diurnal sine generation",
        "Transmits JSON to Cloud every 5-6s."
    ], ACCENT_CYAN)
    add_card(s3, Inches(3.7), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 2: API Gateway", [
        "Amazon API Gateway v2",
        "Lightweight HTTP Protocol",
        "CORS Preflight enabled (*)",
        "PayloadFormatVersion: 2.0",
        "POST /telemetry route",
        "GET /telemetry route",
        "Sub-15ms routing latency."
    ], ACCENT_AMBER)
    add_card(s3, Inches(6.6), Inches(1.8), Inches(2.7), Inches(5.0), "Tier 3: Serverless Compute", [
        "AWS Lambda (Python 3.12)",
        "Memory: 128 MB | Timeout: 10s",
        "Input sanitization & validation",
        "Steadman Heat Index calc",
        "Status categorizer (HEAT, FREEZE, HUMID, NORMAL)",
        "DynamoDBCrudPolicy access."
    ], ACCENT_CYAN)
    add_card(s3, Inches(9.5), Inches(1.8), Inches(3.0), Inches(5.0), "Tier 4: Storage & UI", [
        "Amazon DynamoDB",
        "Table: envirosense-telemetry",
        "Key: deviceId (HASH)",
        "TTL: expiresAt (24 Hours)",
        "Amazon S3 Static Website",
        "Public Read Bucket Policy",
        "HTML5 / CSS3 / JS Dashboard",
        "Real-time SVG trend chart."
    ], ACCENT_GREEN)

    # ================= SLIDE 4: Microcontroller Firmware =================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4)
    add_header(s4, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Microcontroller & Sensor Hardware Ingestion")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "ESP32 DevKit V1 + DHT11 Implementation", [
        "Microcontroller: 32-bit dual-core Xtensa LX6 @ 240MHz with 2.4GHz Wi-Fi.",
        "Sensor Pinout: DHT11 Data line connected to GPIO 4 (3.3V power rail).",
        "OLED Pinout: SSD1306 128x64 display driven via I2C (SDA -> GPIO 21, SCL -> GPIO 22).",
        "Non-blocking Timing: Uses millis() interval timer (every 6000ms) without freeze-delays.",
        "Automatic Reconnection: If Wi-Fi disconnects, background loop re-establishes link gracefully."
    ], ACCENT_CYAN)
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "On-Device Display & HTTP Transmission", [
        "Local OLED Graphics: Renders live Temperature (°C), Humidity (%), Heat Index (°C) and Wi-Fi signal status.",
        "Visual Hazard Alarms: Local OLED displays 'ALERT: HEAT HAZARD!' when temp exceeds 40°C.",
        "ArduinoJson Serialization: Formats compact JSON payload with deviceId and sensor metrics.",
        "HTTP POST Publication: Dispatches payload to API Gateway with Content-Type: application/json.",
        "Zero Cloud Dependency for Local Readouts: Field operators see status even if internet drops."
    ], ACCENT_GREEN)

    # ================= SLIDE 5: Python Edge Simulator =================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5)
    add_header(s5, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Python Edge Sensor Simulator & Test Harness")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Standard-Library Software Simulator", [
        "Zero External Dependencies: Built strictly with Python 3 standard library (urllib, math, random, json).",
        "CLI Flexibility: Configurable arguments: --api-url, --device-id, --location, --interval, --mode.",
        "Safe Dry-Run Mode: '--dry-run' outputs formatted JSON to terminal without sending network requests.",
        "Single-Shot Verification: '--once' sends exactly 1 reading and terminates (ideal for automated CI/CD checks).",
        "Cross-Platform: Runs on Windows, Linux, macOS, and Raspberry Pi without installation hurdles."
    ], ACCENT_AMBER)
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Thermodynamic Simulation Modes", [
        "Normal Mode: Realistic room temperature (22-26°C, 45-55% RH) with natural Brownian noise.",
        "Heatwave Mode: Severe thermal surge (40-44°C, 75-88% RH) generating Heat Index > 80°C.",
        "Freeze Mode: Freezing environmental drop (0-4°C, 28-35% RH) for refrigeration facility tests.",
        "Fluctuate Mode: Mathematical diurnal sine wave simulating day/night ambient temperature drift.",
        "Instant Feedback: Terminal prints timestamped JSON, calculated Heat Index, and HTTP response code."
    ], ACCENT_CYAN)

    # ================= SLIDE 6: Serverless Compute & Lambda =================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6)
    add_header(s6, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Serverless Compute & Persistence (Lambda + DynamoDB)")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "AWS Lambda Ingestion Engine (Python 3.12)", [
        "Event Dispatcher: Routes HTTP API methods (POST /telemetry, GET /telemetry, OPTIONS).",
        "Input Sanitization: Rejects out-of-bounds temperatures (-40°C to +85°C) and bad formats.",
        "Steadman Heat Index Engine: Implements NOAA/Rothfusz regression equation for apparent temperature.",
        "Automated Status Classification: Categorizes readings into NORMAL, HEAT_ALERT, FREEZE_ALERT, and HIGH_HUMIDITY.",
        "Stateless & Auto-Scaling: Scales from zero to thousands of simultaneous sensor nodes seamlessly."
    ], ACCENT_CYAN)
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Amazon DynamoDB with Automated TTL", [
        "NoSQL Schema: Partition Key 'deviceId' (String) stores current state and telemetry history.",
        "Pay-Per-Request Billing: Zero idle cost; charges only per actual read/write operations.",
        "TTL Lifecycle (expiresAt): Automatically deletes records older than 24 hours without custom cron jobs.",
        "Fast Retrieval: Single-digit millisecond query times for instant dashboard updates.",
        "Learner Lab Optimization: Eliminates database bloat, keeping AWS credit spend strictly at $0.00."
    ], ACCENT_GREEN)

    # ================= SLIDE 7: S3 Static Web Dashboard =================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7)
    add_header(s7, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Responsive S3 Static Web Dashboard")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Modern Glassmorphic Architecture", [
        "100% Zero CDN Dependencies: Pure vanilla HTML5, CSS3, and JavaScript.",
        "Air-Gapped & Offline Ready: Loads reliably inside classrooms, offline labs, or S3 public endpoints.",
        "Hero Telemetry Gauges: Large digital displays for Ambient Temp (°C & °F), Humidity (%), and Feels Like Heat Index.",
        "Color-Coded Meter Bars: Smoothly animated visual progress bars reflecting threshold percentages.",
        "Dark Theme UI: Tailored for 24/7 monitoring centers with glowing badges and high contrast."
    ], ACCENT_CYAN)
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Real-Time SVG Chart & Dual Mode", [
        "Native SVG Trendline: Dynamically generates vector curves for the last 10 readings without external chart libraries.",
        "Dual Legend: Cyan line for Temperature (°C), Blue line for Humidity (%).",
        "Interactive Preset Buttons: One-click buttons to simulate Normal, Heatwave, Cold Wave, and High Humidity states.",
        "Continuous Auto-Stream: Generates realistic live ticks every 3 seconds for exhibition demos.",
        "Local Storage Memory: Retains API Gateway URLs and keys in browser memory across page reloads."
    ], ACCENT_AMBER)

    # ================= SLIDE 8: Demonstration: Normal =================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8)
    add_header(s8, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Demonstration: Normal Ambient Climate Monitoring")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Operational Scenario & Baseline Telemetry", [
        "Target Facility: Campus Greenhouse Lab / Computer Lab 102.",
        "Ambient Temperature: 24.5 °C (76.1 °F) — well within normal 18°C-28°C range.",
        "Relative Humidity: 48.0 % — optimal comfort range (ideal is 40%-60%).",
        "Calculated Heat Index: 24.8 °C — zero thermal fatigue risk.",
        "Telemetry Frequency: Data points ingested and plotted every 5 seconds."
    ], ACCENT_GREEN)
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Dashboard & Edge Response", [
        "Header Badge: Displays glowing green 'NORMAL' status indicator.",
        "Summary Box: 'All environmental metrics are within safe operational thresholds.' (Emerald accent).",
        "OLED Node Status: ESP32 display reads 'STATUS: CLIMATE OK' with active Wi-Fi link.",
        "Chronological Log: Records ingested with deviceId 'enviro-node-01' and UTC timestamps.",
        "SVG Trendline: Shows stable, calm wave pattern indicating balanced thermal equilibrium."
    ], ACCENT_CYAN)

    # ================= SLIDE 9: Demonstration: Hazard Alerts =================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9)
    add_header(s9, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Demonstration: Critical Hazard Alerts & Recovery")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Critical Heatwave Simulation (>40°C)", [
        "Triggered Condition: 41.8 °C with 84.0 % Relative Humidity.",
        "Heat Index Spike: Escalates to 94.6 °C thermal danger index.",
        "System Alert State: Switches immediately to pulsing red 'HEAT ALERT'.",
        "Risk Evaluation: 'Risk Level: Danger (Heat Exhaustion / Thermal Stress)'.",
        "OLED Hardware Reaction: Screen flashes 'ALERT: HEAT HAZARD!' to alert room occupants."
    ], ACCENT_RED)
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Cold Wave Simulation & Auto-Recovery", [
        "Freezing Condition: 2.4 °C with 32.0 % Humidity (Frost risk).",
        "System Alert State: Switches to 'FREEZE ALERT' (Risk of pipe freezing / cold damage).",
        "Excess Moisture Event: 29.2 °C with 92.0 % Humidity triggers amber 'HIGH HUMIDITY' caution.",
        "Seamless Recovery: Selecting 'Optimal (24°C)' immediately restores the green NORMAL status.",
        "Dynamic Vector Shift: SVG chart slopes visibly up or down matching temperature swings in real time."
    ], ACCENT_AMBER)

    # ================= SLIDE 10: Terminal Testing & Verification =================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10)
    add_header(s10, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Terminal Execution, Unit Testing & Verification")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Automated Unit Test Suite (tests/test_lambda.py)", [
        "Framework: Python unittest with mock DynamoDB and boto3 resources.",
        "TC-01: Valid telemetry POST stores item and calculates Heat Index [PASS].",
        "TC-02: Extreme temperature (>40°C) triggers HEAT_ALERT classification [PASS].",
        "TC-03: Low temperature (<=5°C) triggers FREEZE_ALERT classification [PASS].",
        "TC-04: Out-of-bounds temperature (-95°C) safely rejected with HTTP 400 [PASS].",
        "TC-05: Missing humidity attribute rejected with HTTP 400 [PASS].",
        "TC-06: GET /telemetry returns chronological history [PASS].",
        "TC-07: CORS preflight (OPTIONS) returns HTTP 204 with wildcard headers [PASS]."
    ], ACCENT_CYAN)
    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Execution Performance & Verification Metrics", [
        "Test Execution Speed: All 7 test cases execute in 0.002 seconds.",
        "Zero Cloud Dependency: Tests run offline on clean workstations without AWS tokens.",
        "Simulator Verification: python simulator/simulator.py --dry-run --once generates valid JSON.",
        "HTTP Server Verification: Local web server serves dashboard with HTTP 200 OK on port 8080.",
        "100% Pass Rate: Zero warnings, zero errors, fully regression-free."
    ], ACCENT_GREEN)

    # ================= SLIDE 11: Cost & Free Tier Analysis =================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11)
    add_header(s11, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Comprehensive AWS Cost & Free Tier Analysis")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "AWS Free Tier Monthly Allowances", [
        "AWS Lambda: 1,000,000 requests/month & 3.2M seconds compute FREE.",
        "Amazon DynamoDB: 25 GB storage + 25 Write & Read Capacity Units FREE.",
        "Amazon S3: 5 GB Standard Storage + 20,000 GET requests FREE.",
        "Amazon API Gateway: 1,000,000 HTTP API calls/month FREE.",
        "AWS CloudWatch: 10 custom metrics + 5 GB log ingestion FREE."
    ], ACCENT_GREEN)
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "EnviroSense Operational Monthly Usage", [
        "1 Sensor Node @ 6s interval = ~432,000 requests/month (within 1M free tier).",
        "Lambda Execution Time: Avg 15ms per call @ 128MB = ~6,480 GB-s (vastly below 400,000 GB-s).",
        "DynamoDB Storage with 24h TTL = ~14,400 active items (~4.3 MB total, << 25 GB).",
        "S3 Static Site: Static frontend footprint is <50 KB total.",
        "Net Monthly Cost in AWS Learner Lab: $0.00 (100% Free Tier Eligible)."
    ], ACCENT_AMBER)

    # ================= SLIDE 12: Project Limitations & Solutions 1 =================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12)
    add_header(s12, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Project Limitations & Engineering Solutions — Part 1")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Limitation 1: Hardware Availability for Exam Demos", [
        "Challenge: Microcontrollers or lab breadboards may not be available during oral presentations.",
        "ENGINEERING SOLUTION:",
        "• Engineered a built-in browser-based Interactive Demo Engine inside the frontend.",
        "• Developed a cross-platform Python CLI simulator with multiple weather modes.",
        "• Students can demonstrate 100% of product features using just a standard laptop browser."
    ], ACCENT_CYAN)
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Limitation 2: AWS Learner Lab Session Expirations", [
        "Challenge: Learner Lab credentials expire after 4 hours, causing API authentication dropouts.",
        "ENGINEERING SOLUTION:",
        "• Automated deployment script (deploy.ps1) with fast CloudFormation packaging.",
        "• Graceful dashboard fallback: Automatically shifts to Demo Mode if cloud API token expires.",
        "• LocalStorage saves API URLs so users don't need to re-type endpoints upon reconnection."
    ], ACCENT_AMBER)

    # ================= SLIDE 13: Project Limitations & Solutions 2 =================
    s13 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s13)
    add_header(s13, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Project Limitations & Engineering Solutions — Part 2")
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Limitation 3: DynamoDB Storage Accumulation", [
        "Challenge: Continuous 6-second sensor pings generate 14,400 items per day per node.",
        "ENGINEERING SOLUTION:",
        "• Integrated native DynamoDB Time-To-Live (TTL) on attribute 'expiresAt'.",
        "• Items expire and purge automatically after 86,400 seconds (24 hours).",
        "• Eliminates maintenance overhead and guarantees zero storage bloat."
    ], ACCENT_CYAN)
    add_card(s13, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Limitation 4: Learner Lab IAM Role Creation Block", [
        "Challenge: Learner Lab rejects IAM role creation requests in CloudFormation.",
        "ENGINEERING SOLUTION:",
        "• Codified cloudformation.yaml with 'UseLabRole: true' parameter.",
        "• Attaches pre-existing 'arn:aws:iam::<account>:role/LabRole' automatically.",
        "• SAM and CloudFormation deploy cleanly without permission denials."
    ], ACCENT_GREEN)

    # ================= SLIDE 14: Academic Deliverables =================
    s14 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s14)
    add_header(s14, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Academic Deliverables & Submission Package")
    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Document & Reporting Deliverables", [
        "1. Product Start Sheet: PRODUCT_START_SHEET.docx (Formal course sheet).",
        "2. Complete Product Report: PRODUCT_REPORT.docx (Full 6-section report).",
        "3. Hardware Wiring Schematic: wiring_schematic.md (ESP32 ASCII circuit diagram).",
        "4. Master README: README.md (Setup, architecture, tests & guides).",
        "5. Presentation Deck: EnviroSense_Master_Presentation.pptx (This 16-slide deck)."
    ], ACCENT_CYAN)
    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Cloud, Code & Hardware Deliverables", [
        "6. AWS SAM Infrastructure: template.yaml & samconfig.toml.",
        "7. Pure CloudFormation: cloudformation.yaml (With Learner Lab LabRole).",
        "8. Microcontroller C++ Firmware: esp32_dht11_oled.ino.",
        "9. Python Edge Simulator: simulator/simulator.py.",
        "10. Automated Unit Test Suite: tests/test_lambda.py (100% pass).",
        "11. S3 Web Dashboard: frontend/ (index.html, styles.css, app.js).",
        "12. GitHub Repository: https://github.com/yeshwanthkushi25-glitch/envirosense-iot-dashboard."
    ], ACCENT_GREEN)

    # ================= SLIDE 15: Step-by-Step Demo Walkthrough =================
    s15 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s15)
    add_header(s15, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Step-by-Step Live Demonstration Walkthrough")
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Demo Sequence 1: Offline Browser Demo", [
        "1. Open frontend/index.html (or http://localhost:8080).",
        "2. Show initial baseline reading: 24.5 °C, 48% Humidity, NORMAL status.",
        "3. Click '🔥 Heatwave': Notice status turning pulsing RED ('HEAT ALERT').",
        "4. Point out the Steadman Heat Index escalating past 40°C danger zone.",
        "5. Click '❄️ Cold Wave': Notice status shifting to 'FREEZE ALERT'.",
        "6. Click '▶️ Start Live Stream': Watch the real-time SVG chart plot dynamic sensor curves every 3 seconds."
    ], ACCENT_AMBER)
    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Demo Sequence 2: Edge Simulator & AWS Cloud", [
        "1. Open terminal and run: python simulator/simulator.py --dry-run --once.",
        "2. Show formatted JSON payload with deviceId, location, and computed heatIndex.",
        "3. Connect ESP32 hardware or run simulator with live API Gateway URL.",
        "4. Paste API Gateway URL into the dashboard and click 'Connect to AWS'.",
        "5. Badge shifts to 'AWS CONNECTED'; dashboard polls live DynamoDB records in real time.",
        "6. Show DynamoDB console displaying time-series records and TTL timestamps."
    ], ACCENT_CYAN)

    # ================= SLIDE 16: Conclusion & Team Contributions =================
    s16 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s16)
    add_header(s16, "SR University · Cloud Computing (25CAI102PC205) · Product No. 23", "Conclusion & Team Contributions")
    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "M. Yeshwanth (H.T. No: 2503A53005)", [
        "• Researched course syllabus and selected Product #23 (IoT Environmental Dashboard).",
        "• Authored production ESP32 Arduino C++ firmware (esp32_dht11_oled.ino).",
        "• Designed complete hardware wiring schematic and I2C pinout documentation.",
        "• Developed Python edge sensor simulator (simulator.py) with atmospheric algorithms.",
        "• Validated multi-mode sensor streaming (Normal, Heatwave, Freeze, Fluctuate).",
        "• Configured Git repository, deployment scripts, and project packaging."
    ], ACCENT_CYAN)
    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "V. Laxmiprasad (H.T. No: 2503A53006)", [
        "• Engineered AWS Lambda backend with Steadman Heat Index calculations (backend/app.py).",
        "• Codified CloudFormation (cloudformation.yaml) & SAM (template.yaml) with LabRole.",
        "• Configured Amazon DynamoDB with automated 24-hr TTL lifecycle management.",
        "• Developed S3 static glassmorphic dashboard with native SVG charting (frontend/).",
        "• Authored automated unit test suite (tests/test_lambda.py) achieving 100% pass rate.",
        "• Compiled academic documentation and master presentation deck."
    ], ACCENT_GREEN)

    # Save
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\yeshwanth\OneDrive\Desktop\cloud product 2\cloud computing product 2"
    create_deck(os.path.join(out_dir, "EnviroSense_Master_Presentation.pptx"))
