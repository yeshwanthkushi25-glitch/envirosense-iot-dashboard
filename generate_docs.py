import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_start_sheet(output_path):
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Header
    p_uni = doc.add_paragraph()
    r_uni = p_uni.add_run("Cloud Computing (25CAI102PC205) · SR University")
    r_uni.font.name = "Calibri"
    r_uni.font.size = Pt(14)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(14, 116, 144)

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("Product Start Sheet (Course Product #23)")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run("Product No.: 23    |    Title: EnviroSense — IoT Climate & Air Quality Dashboard\nTeam Name: EnviroSense    |    Batch: 59    |    Environment: AWS Learner Lab (us-east-1)")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(10.5)
    r_meta.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # Team Members Table
    p_h = doc.add_paragraph()
    r_h = p_h.add_run("Team Members & Roles")
    r_h.font.name = "Calibri"
    r_h.font.size = Pt(12)
    r_h.font.bold = True
    r_h.font.color.rgb = RGBColor(14, 116, 144)

    table1 = doc.add_table(rows=3, cols=3)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = False

    headers1 = ["Member Name", "H.T. No.", "What I Will Do"]
    for i, h in enumerate(headers1):
        cell = table1.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0E7490")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        p.runs[0].font.name = "Calibri"
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    rows_data1 = [
        ("M. Yeshwanth", "2503A53005", "Develop ESP32 C++ firmware (PlatformIO), wire DHT22 + MQ-135 + SSD1306 OLED, author Wokwi VS Code virtual circuit (diagram.json), configure CloudFormation stack in us-east-1, and manage Git repository."),
        ("V. Laxmiprasad", "2503A53006", "Develop AWS Lambda validation engine (Python 3.12), implement Steadman Heat Index & gas hazard classification, configure DynamoDB 24-hr TTL lifecycle, design S3 glassmorphic dashboard (frontend/), and author 8-case automated unit test suite.")
    ]

    for row_idx, data in enumerate(rows_data1):
        bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = table1.cell(row_idx + 1, col_idx)
            cell.text = text
            set_cell_background(cell, bg)
            set_cell_margins(cell, 100, 100, 150, 150)
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Calibri"
            p.runs[0].font.size = Pt(9.5)

    table1.columns[0].width = Inches(1.8)
    table1.columns[1].width = Inches(1.3)
    table1.columns[2].width = Inches(3.6)

    doc.add_paragraph()

    # Section 1
    p = doc.add_paragraph()
    r = p.add_run("1. Our product in one sentence")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)
    p_body = doc.add_paragraph("Our product helps campus laboratories, agricultural greenhouse facilities, and server rooms monitor temperature, relative humidity, apparent heat index, and toxic gas/air quality (PPM) in real time using AWS serverless cloud infrastructure and dual physical/virtual ESP32 edge telemetry nodes.")
    p_body.runs[0].font.name = "Calibri"; p_body.runs[0].font.size = Pt(10.5)

    # Section 2
    p = doc.add_paragraph()
    r = p.add_run("2. Who will use it, and what problem does it solve?")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)
    p_body = doc.add_paragraph(
        "Target Users: Agricultural greenhouse managers, university laboratory instructors, cleanroom supervisors, and IT data center technicians.\n\n"
        "Problem Solved: Traditional environmental monitoring is manual, unrecorded, and localized. When facilities overheat, experience severe humidity spikes, or develop toxic solvent gas leaks, equipment degrades and biological specimens spoil before personnel notice. EnviroSense provides continuous automated multi-sensor sampling (DHT22 + MQ-135), computes the Steadman Heat Index ('Feels Like') server-side, flags critical thermal and chemical hazards in real time, and renders live vector trend curves on an S3-hosted glassmorphic dashboard accessible from any web browser."
    )
    p_body.runs[0].font.name = "Calibri"; p_body.runs[0].font.size = Pt(10.5)

    # Section 3
    p = doc.add_paragraph()
    r = p.add_run("3. Draw your idea in 3–5 boxes")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)
    p_body = doc.add_paragraph(
        "Data Flow Architecture:\n"
        "1. ESP32 Node (DHT22 + MQ-135 + OLED) or Wokwi VS Code Virtual Simulator\n"
        "   └──> 2. Amazon API Gateway (HTTP API v2, sub-15ms proxy routing)\n"
        "        └──> 3. AWS Lambda (Python 3.12 Validator, Heat Index & Gas Alert Engine)\n"
        "             └──> 4. Amazon DynamoDB (NoSQL Time-Series Store with 24-hr TTL)\n"
        "                  └──> 5. Amazon S3 Static Dashboard (4 circular radial gauges, SVG charts, and Web Audio siren alerts)\n\n"
        "*Note: A virtual Wokwi simulation in VS Code and an interactive offline Demo Engine with 5 scenario presets are built in for instant live presentation without requiring physical breadboards."
    )
    p_body.runs[0].font.name = "Calibri"; p_body.runs[0].font.size = Pt(10.5)

    # Section 4
    p = doc.add_paragraph()
    r = p.add_run("4. AWS services we will use, and why")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)

    table2 = doc.add_table(rows=6, cols=2)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.autofit = False

    headers2 = ["AWS Service", "Why We Need It in OUR Product"]
    for i, h in enumerate(headers2):
        cell = table2.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0E7490")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        p.runs[0].font.name = "Calibri"; p.runs[0].font.bold = True; p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    services_data = [
        ("AWS Lambda", "Executes serverless Python 3.12 functions to sanitize sensor payloads, calculate Steadman Heat Index, evaluate multi-tier alert states (HEAT_ALERT, FREEZE_ALERT, GAS_ALERT), and format DynamoDB Decimal items."),
        ("Amazon API Gateway (v2)", "Provides low-latency HTTP API routes (POST /telemetry, GET /telemetry, OPTIONS CORS) for edge devices, Wokwi virtual nodes, and browser dashboards."),
        ("Amazon DynamoDB", "Maintains time-series environmental records keyed by deviceId with Pay-Per-Request pricing and native 24-hr Time-to-Live (TTL) for zero-cost automated data pruning."),
        ("Amazon S3 Static Website", "Hosts the zero-dependency dark-mode dashboard (index.html, styles.css, app.js) publicly without requiring expensive or persistent EC2 virtual servers."),
        ("AWS CloudFormation", "Codifies reproducible Infrastructure-as-Code pre-configured with AWS Learner Lab LabRole permissions for zero-friction cloud deployment.")
    ]

    for row_idx, (srv, desc) in enumerate(services_data):
        bg = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        for col_idx, text in enumerate([srv, desc]):
            cell = table2.cell(row_idx + 1, col_idx)
            cell.text = text
            set_cell_background(cell, bg)
            set_cell_margins(cell, 100, 100, 150, 150)
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Calibri"; p.runs[0].font.size = Pt(9.5)
            if col_idx == 0: p.runs[0].font.bold = True

    table2.columns[0].width = Inches(2.2)
    table2.columns[1].width = Inches(4.5)

    doc.add_paragraph()

    # Section 5 & 6
    p = doc.add_paragraph()
    r = p.add_run("5. The FIRST small thing we will build")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)
    p_body = doc.add_paragraph("Transmit a simulated temperature/humidity/gas JSON reading from the virtual ESP32 node to the Lambda API, calculate the heat index, and reflect it immediately as a green normal reading on the local and S3 dashboard.")
    p_body.runs[0].font.name = "Calibri"; p_body.runs[0].font.size = Pt(10.5)

    p = doc.add_paragraph()
    r = p.add_run("6. Project Expo & Oral Evaluation Readiness")
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)
    p_body = doc.add_paragraph(
        "Status: Yes, our team is 100% ready.\n\n"
        "What we will show working:\n"
        "• Demonstrate normal ambient monitoring with real-time animated circular radial meters and native SVG waveforms.\n"
        "• Slide the DHT22 temperature to 42°C in VS Code Wokwi and show immediate transition to pulsing red 'HEAT ALERT' with thermal danger warnings.\n"
        "• Slide the MQ-135 gas sensor to 750 PPM to trigger acoustic Web Audio siren and 'GAS ALERT' hazard state.\n"
        "• Demonstrate zero-hardware Wokwi simulation running in VS Code with direct HTTPS transmission to Amazon AWS.\n"
        "• Present 8 automated unit tests passing 100% offline in 0.005 seconds."
    )
    p_body.runs[0].font.name = "Calibri"; p_body.runs[0].font.size = Pt(10.5)

    doc.save(output_path)
    print(f"Start Sheet saved to: {output_path}")

def create_product_report(output_path, img_dir):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    # University Header
    p_top = doc.add_paragraph()
    r = p_top.add_run("SR UNIVERSITY · CLOUD COMPUTING (25CAI102PC205)")
    r.font.name = "Calibri"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)

    p_title = doc.add_paragraph()
    r = p_title.add_run("PRODUCT REPORT: EnviroSense — IoT Climate & Air Quality Dashboard")
    r.font.name = "Calibri"; r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = RGBColor(15, 23, 42)

    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Course Product No.: 23    |    Batch: 59    |    Environment: AWS Learner Lab (us-east-1)\nTeam Members: M. Yeshwanth (2503A53005) & V. Laxmiprasad (2503A53006)")
    r.font.name = "Calibri"; r.font.size = Pt(10.5); r.font.color.rgb = RGBColor(71, 85, 105)

    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title)
        r.font.name = "Calibri"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = RGBColor(14, 116, 144)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = "Calibri"; r.font.size = Pt(10); r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_figure(img_filename, caption):
        img_path = os.path.join(img_dir, img_filename)
        if os.path.exists(img_path):
            doc.add_paragraph().paragraph_format.space_before = Pt(8)
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(img_path, width=Inches(5.8))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Calibri"
            r_cap.font.size = Pt(9.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = RGBColor(71, 85, 105)

    # Section 1
    add_section_header("1. Product Overview")
    add_body(
        "1.1 Problem Solved:\n"
        "In university agricultural greenhouses, biological tissue incubation cleanrooms, and data-center computer laboratories, microclimate fluctuations and airborne chemical hazards pose critical risks to expensive hardware and biological research. Traditional monitoring relies on isolated analogue thermometer checks or disconnected local sensors. These readings are ephemeral, unaggregated, and impossible to audit remotely. EnviroSense resolves this by streaming continuous sensor telemetry (DHT22 temperature & humidity, MQ-135 air quality/gas) to an AWS serverless cloud architecture, offering centralized monitoring, automated hazard classification, and live web visualization."
    )
    add_body(
        "1.2 Objective:\n"
        "To construct a production-grade, serverless cloud IoT platform that ingests environmental data via an HTTP API, performs server-side Steadman Heat Index computations and gas toxicity evaluations, enforces automated TTL data lifecycle management in DynamoDB, and renders real-time telemetry on an S3 static web dashboard featuring a built-in offline Demo Mode."
    )
    add_body(
        "1.3 Target Users:\n"
        "• Campus and Laboratory Administrators: Overseeing hardware thermal safety in computer labs.\n"
        "• Greenhouse Operators: Tracking microclimates, moisture thresholds, and ambient heat curves.\n"
        "• Chemical & Biological Lab Technicians: Monitoring volatile organic compounds (VOCs) and solvent fume leaks."
    )

    # Section 2
    add_section_header("2. Architecture and Technologies")
    add_body(
        "Architecture & Data Flow:\n"
        "1. Edge Ingestion Layer: A DOIT ESP32 microcontroller (or Wokwi virtual simulator in VS Code) samples DHT22 and MQ-135 sensors every 2 seconds and dispatches an HTTP POST JSON payload to API Gateway.\n"
        "2. API Gateway (HTTP API v2): Ingests the payload, validates CORS preflights, and proxies requests to AWS Lambda with sub-15ms latency.\n"
        "3. AWS Lambda Compute: Sanitizes inputs (-40°C to +85°C, 0-100% RH, 0-10000 PPM), calculates the Steadman Heat Index, evaluates alert thresholds (HEAT_ALERT, FREEZE_ALERT, GAS_ALERT), and appends a 24-hr TTL timestamp.\n"
        "4. Amazon DynamoDB: Persists the structured record into 'envirosense-telemetry' with Pay-Per-Request capacity and automatic TTL expiration.\n"
        "5. Amazon S3 Static Dashboard: Queries GET /telemetry every 1 second to update 4 circular radial meters, animated status banners, and native SVG waveforms."
    )

    add_figure("architecture-diagram.png", "Figure 1: EnviroSense 4-Tier Serverless Cloud Architecture Diagram")
    add_figure("hardware-schematic.png", "Figure 2: ESP32 DevKit V1 Hardware Circuit & Sensor Pinout Schematic (DHT22 + MQ-135 + OLED)")
    add_figure("thermal-heat-matrix.png", "Figure 3: NOAA / Steadman Apparent Heat Index Risk Calculation Spectrum")

    # Technologies Table
    t_tech = doc.add_table(rows=7, cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_headers = ["AWS Service / Component", "Role in EnviroSense", "Configuration / Runtime"]
    for i, h in enumerate(tech_headers):
        c = t_tech.cell(0, i)
        c.text = h
        set_cell_background(c, "0E7490")
        set_cell_margins(c, 100, 100, 120, 120)
        c.paragraphs[0].runs[0].font.name = "Calibri"
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    tech_data = [
        ("Amazon API Gateway (v2)", "Ingests telemetry from edge devices and serves dashboard queries", "HTTP API, CORS enabled (*), auto-deployed stage $default"),
        ("AWS Lambda", "Validates input, calculates Steadman Heat Index, formats DB item", "Python 3.12, 128 MB RAM, 10s timeout, LabRole execution"),
        ("Amazon DynamoDB", "NoSQL time-series data storage with automated lifecycle pruning", "Pay-Per-Request, HASH: deviceId, TTL: expiresAt (24h)"),
        ("Amazon S3 Static Website", "Hosts frontend assets publicly with zero maintenance servers", "WebsiteConfiguration (index.html), public-read bucket policy"),
        ("ESP32 Embedded C++", "Physical field telemetry node with local I2C OLED display", "Xtensa 240MHz, DHT22 on GPIO 4, MQ-135 on GPIO 34, SSD1306 on I2C"),
        ("Wokwi VS Code Simulator", "Virtual hardware breadboard simulation in VS Code", "diagram.json + wokwi.toml, Wokwi-GUEST Wi-Fi, direct AWS link")
    ]
    for r_idx, row in enumerate(tech_data):
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = t_tech.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 120, 120)
            cell.paragraphs[0].runs[0].font.name = "Calibri"
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if c_idx == 0: cell.paragraphs[0].runs[0].font.bold = True

    t_tech.columns[0].width = Inches(2.0)
    t_tech.columns[1].width = Inches(2.8)
    t_tech.columns[2].width = Inches(2.0)

    # Section 3
    add_section_header("3. Implementation and Cloud Deployment")
    add_body(
        "Deployment in AWS Learner Lab:\n"
        "AWS Learner Lab imposes strict sandbox security policies, notably prohibiting students from creating or modifying IAM roles. To eliminate deployment failures, our CloudFormation (cloudformation.yaml) stack is codified with a 'UseLabRole: true' parameter. This attaches the pre-configured 'arn:aws:iam::683495019184:role/LabRole' to Lambda functions automatically.\n\n"
        "Live Deployment Specifications:\n"
        "• GitHub Repository: https://github.com/yeshwanthkushi25-glitch/envirosense-iot-dashboard\n"
        "• Live Ingestion API: https://etejnaemlc.execute-api.us-east-1.amazonaws.com/telemetry\n"
        "• Live S3 Static Dashboard: http://envirosense-dashboard-683495019184.s3-website-us-east-1.amazonaws.com\n"
        "• DynamoDB Table: envirosense-telemetry (On-Demand, TTL enabled)\n"
        "• AWS Region: us-east-1 (Account: 683495019184)"
    )

    # Section 4
    add_section_header("4. Testing and Verification Results")
    add_body(
        "Visual Demonstration Screenshots & Test Cases:\n"
        "The figures below illustrate the live operational states of the EnviroSense S3 dashboard and terminal verification suites."
    )

    add_figure("dashboard-operational-green.png", "Figure 4: EnviroSense Dashboard — Operational Normal State (Glowing Green, 4 Radial Meters)")
    add_figure("dashboard-failure-red.png", "Figure 5: EnviroSense Dashboard — Critical Hazard State (Gas Leak & Heat Alert with Siren)")
    add_figure("terminal-monitor-demo.png", "Figure 6: Automated Unit Test Suite (8/8 PASS in 0.005s) & Edge Simulator Execution")

    t_tests = doc.add_table(rows=9, cols=4)
    t_tests.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Test ID", "Scenario Description", "Expected Outcome", "Status"]
    for i, h in enumerate(test_headers):
        c = t_tests.cell(0, i)
        c.text = h
        set_cell_background(c, "0E7490")
        set_cell_margins(c, 100, 100, 120, 120)
        c.paragraphs[0].runs[0].font.name = "Calibri"
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    test_rows = [
        ("TC-01", "Standard Telemetry POST (24.5°C, 48% RH, 180 PPM)", "HTTP 201; Heat Index calculated; status NORMAL", "PASS"),
        ("TC-02", "Heatwave Condition (42.0°C, 85% RH)", "HTTP 201; Status classified as HEAT_ALERT", "PASS"),
        ("TC-03", "Cold Wave Condition (2.0°C, 30% RH)", "HTTP 201; Status classified as FREEZE_ALERT", "PASS"),
        ("TC-04", "Toxic Gas Leak Condition (750 PPM Gas)", "HTTP 201; Status classified as GAS_ALERT hazard", "PASS"),
        ("TC-05", "Out-of-Bounds Sensor Temperature (-95°C)", "HTTP 400 Bad Request; DynamoDB put rejected", "PASS"),
        ("TC-06", "Missing Required Humidity Field", "HTTP 400 Bad Request; Descriptive error returned", "PASS"),
        ("TC-07", "Telemetry Retrieval via GET /telemetry", "HTTP 200 OK; Returns array sorted by timestamp", "PASS"),
        ("TC-08", "HTTP CORS Preflight (OPTIONS)", "HTTP 204 No Content; Wildcard origin allowed (*)", "PASS")
    ]
    for r_idx, row in enumerate(test_rows):
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = t_tests.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 120, 120)
            cell.paragraphs[0].runs[0].font.name = "Calibri"
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if c_idx == 3: cell.paragraphs[0].runs[0].font.bold = True; cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(16, 185, 129)

    t_tests.columns[0].width = Inches(0.9)
    t_tests.columns[1].width = Inches(2.8)
    t_tests.columns[2].width = Inches(2.4)
    t_tests.columns[3].width = Inches(0.7)

    # Section 5
    add_section_header("5. Challenges and Conclusion")
    add_body(
        "Key Engineering Challenges & Solutions:\n"
        "1. Physical Hardware Independence: Lab examinations frequently occur in lecture halls without Wi-Fi breadboards. We solved this by developing an interactive in-browser Demo Engine with one-click weather presets and a Wokwi VS Code virtual hardware simulator, guaranteeing full demonstration capability on any laptop.\n"
        "2. Learner Lab IAM Limitations: CloudFormation stacks failed when requesting custom IAM roles. We introduced the 'UseLabRole: true' parameter to attach the pre-existing LabRole automatically.\n"
        "3. High-Frequency Telemetry Accumulation: Continuous sensor streaming quickly amasses tens of thousands of items. We enabled DynamoDB Time-To-Live (TTL) on 'expiresAt', which purges items after 24 hours at zero compute cost.\n"
        "4. Client-Side Charting without CDN: Most online charting libraries require heavy external CDN script tags that fail in air-gapped university labs. We engineered custom responsive SVG sparklines and radial meters built into vanilla JavaScript.\n\n"
        "Conclusion & Learning Outcomes:\n"
        "The team successfully designed, tested, and documented a full-scale serverless IoT environmental monitoring platform. We mastered AWS Lambda, API Gateway v2, DynamoDB TTL, Infrastructure-as-Code automation, ESP32 embedded C++ programming, Wokwi virtual circuit simulation, and responsive web visualization."
    )

    # Section 6
    add_section_header("6. Team Contributions and References")
    add_body(
        "Team Responsibilities:\n"
        "• M. Yeshwanth (2503A53005): Programmed ESP32 C++ firmware (firmware/src/main.cpp); drafted circuit pinout schematic; configured Wokwi virtual simulator (diagram.json); deployed AWS CloudFormation stack; executed multi-mode telemetry tests; configured Git repository.\n"
        "• V. Laxmiprasad (2503A53006): Built the AWS Lambda backend and Steadman Heat Index engine (backend/app.py); codified DynamoDB Decimal types and TTL pruning; implemented S3 glassmorphic dashboard (frontend/); authored the 8-case unit test suite.\n\n"
        "References:\n"
        "1. NOAA National Weather Service: The Heat Index Equation & Rothfusz Regression Analysis.\n"
        "2. AWS Lambda Developer Guide: Serverless Computing with Python 3.12, AWS Documentation.\n"
        "3. Amazon DynamoDB Developer Guide: Expiring Items with DynamoDB Time to Live (TTL).\n"
        "4. Espressif Systems: ESP32 Wi-Fi & HTTPClient Technical Reference.\n"
        "5. SR University Cloud Computing (25CAI102PC205) Course Laboratory Curriculum."
    )

    doc.save(output_path)
    print(f"Product Report with Embedded Figures saved to: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\yeshwanth\OneDrive\Desktop\cloud product 2\cloud computing product 2\docs"
    img_dir = os.path.join(out_dir, "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    create_start_sheet(os.path.join(out_dir, "PRODUCT_START_SHEET.docx"))
    create_product_report(os.path.join(out_dir, "PRODUCT_REPORT.docx"), img_dir)
