# EnviroSense — IoT Climate & Environmental Dashboard

> **Course**: Cloud Computing (25CAI102PC205) · **Product #23** · **SR University**  
> **Architecture**: ESP32 / Python Edge Simulator → AWS API Gateway → AWS Lambda (Python 3.12) → Amazon DynamoDB → Amazon S3 Static Dashboard

---

## Overview

**EnviroSense** is an end-to-end cloud-native IoT environmental monitoring system designed to track ambient temperature, relative humidity, and Steadman heat index in real time.

Field sensors (physical **ESP32 microcontroller** or cross-platform **Python software simulator**) stream telemetry to an **AWS HTTP API Gateway**. A serverless **AWS Lambda** function validates readings, computes thermal risk indices, triggers alert states (Heat Danger, Freeze Alert, Excessive Humidity), and persists time-series data into **Amazon DynamoDB** with automatic 24-hour Time-to-Live (TTL). The real-time glassmorphic dashboard is hosted as an **Amazon S3 static website**, complete with animated gauges, native SVG sparkline trendlines, and a self-contained **offline Demo Mode** for presentations without active cloud connectivity.

---

## Repository Layout

```text
cloud computing product 2/
├── backend/
│   ├── app.py                 # Lambda handler for validation, heat index, and DynamoDB operations
│   └── requirements.txt       # Python runtime dependencies (boto3)
├── frontend/
│   ├── index.html             # S3-compatible static dashboard (zero CDN dependencies)
│   ├── styles.css             # Glassmorphic dark-theme responsive design
│   └── app.js                 # API Gateway polling, SVG charting, and local demo engine
├── firmware/
│   ├── esp32_dht11_oled.ino   # Production ESP32 Arduino C++ firmware (DHT11 + SSD1306 OLED)
│   └── wiring_schematic.md    # Circuit wiring schematic and hardware pinout table
├── simulator/
│   └── simulator.py           # Cross-platform Python edge sensor simulator with CLI flags
├── tests/
│   └── test_lambda.py         # Offline unit tests for Lambda contract and validation
├── template.yaml              # AWS SAM / CloudFormation infrastructure specification
├── samconfig.toml             # Preconfigured deployment settings (Learner Lab us-east-1)
├── deploy.ps1                 # One-click PowerShell deployment & S3 sync script
├── README.md                  # Comprehensive project documentation (this file)
└── REPORT.md                  # Academic submission report formatted to course guidelines
```

---

## Run the Dashboard Immediately (Zero-Setup Demo)

You can run and test the full dashboard right now without deploying to AWS:

1. Double-click or open `frontend/index.html` in any web browser.
2. It starts automatically in **Demo Mode**, displaying live gauges, heat index calculations, and real-time SVG charts.
3. Test the interactive simulation buttons:
   - **🟢 Optimal (24°C, 48%)**: Normal ambient climate.
   - **🔥 Heatwave (41°C, 84%)**: Simulates severe heat danger; status changes to `HEAT ALERT`.
   - **❄️ Cold Wave (2°C, 32%)**: Simulates freezing conditions; status changes to `FREEZE ALERT`.
   - **💧 High Humidity (29°C, 92%)**: Simulates high condensation risks.
   - **▶️ Start Live Stream**: Starts an automated simulation stream updating every 3 seconds.

---

## Deploy to AWS Learner Lab

### Prerequisites
- AWS CLI v2 (`aws --version`)
- Python 3.10+
- Active AWS Learner Lab credentials configured for `us-east-1` in `~/.aws/credentials`

### Option A: One-Click Automated Script (Recommended)
Open PowerShell in this directory and run:
```powershell
.\deploy.ps1
```
This script automatically:
1. Validates your AWS session.
2. Builds and deploys the CloudFormation / SAM stack (`envirosense`).
3. Extracts the generated API Gateway URL and S3 bucket name.
4. Uploads all `frontend/` files to the S3 bucket with `aws s3 sync`.
5. Prints the public website URL.

### Option B: Guided AWS SAM CLI
```bash
sam build
sam deploy --guided
```
Accept the defaults:
- **Stack Name**: `envirosense`
- **AWS Region**: `us-east-1`
- **Confirm changes before deploy**: `N`
- **Allow SAM CLI IAM role creation**: `Y`

Once deployed, copy the `DashboardBucketName` and `EnviroApiUrl` from the outputs, and upload the frontend:
```bash
aws s3 sync frontend/ s3://YOUR_DASHBOARD_BUCKET_NAME --delete
```

Open the `DashboardWebsiteUrl` in your browser, paste the `EnviroApiUrl` into the API Gateway field, and click **Connect to AWS**.

---

## Microcontroller Hardware Setup (ESP32 + DHT11 + OLED)

If you have physical hardware:
1. Connect components according to [firmware/wiring_schematic.md](file:///c:/Users/yeshwanth/OneDrive/Desktop/cloud%20product%202/cloud%20computing%20product%202/firmware/wiring_schematic.md):
   - **DHT11 Data Pin** → `GPIO 4`
   - **OLED SDA** → `GPIO 21`
   - **OLED SCL** → `GPIO 22`
   - **Power Rails** → `3V3` and `GND`
2. Open `firmware/esp32_dht11_oled.ino` in Arduino IDE.
3. Update `WIFI_SSID`, `WIFI_PASSWORD`, and `API_URL`.
4. Upload the sketch. The OLED display will render real-time temperature, humidity, and transmit JSON to your cloud API every 6 seconds.

---

## Python Edge Simulator (Software Testing)

If you don't have physical hardware, use the included Python simulator:

```powershell
# Single test run (dry run without AWS)
python simulator\simulator.py --dry-run --once

# Stream simulated heatwave to live AWS API Gateway
python simulator\simulator.py --api-url "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com" --mode heatwave

# Realistic day/night diurnal temperature cycle
python simulator\simulator.py --api-url "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com" --mode fluctuate --interval 4
```

---

## Offline Verification & Unit Tests

Run the test suite offline without requiring an active AWS connection:
```powershell
python -m unittest discover -s tests -v
```

All 7 test cases verify:
- Ingestion and schema validation of temperature and humidity.
- Accurate calculation of Steadman Heat Index.
- Automated alert classification (`NORMAL`, `HEAT_ALERT`, `FREEZE_ALERT`, `HIGH_HUMIDITY`).
- Safe rejection of invalid inputs and out-of-bounds readings.
- HTTP CORS preflight compliance (`OPTIONS`).

---

## Expo & Presentation Walkthrough

When demonstrating to instructors or project evaluators:
1. **Show the S3 Dashboard**: Open `frontend/index.html` (or deployed S3 URL). Point out the real-time gauges, heat index risk evaluation, and native SVG trend chart.
2. **Demonstrate Threshold Alerting**: Click **Heatwave Alert (41°C)** — point out how the status pill turns red (`HEAT ALERT`) and the risk evaluation updates.
3. **Demonstrate Recovery**: Click **Optimal (24°C)** — show how the system transitions smoothly back to `NORMAL`.
4. **Explain Cloud Architecture**: Point to `template.yaml` and explain the decoupled, serverless flow:
   - S3 handles static web assets with zero server maintenance.
   - API Gateway provides low-latency HTTP ingestion.
   - Lambda validates and computes metrics on-demand without idle server costs.
   - DynamoDB stores time-series data with automated TTL pruning after 24 hours.
5. **Show Hardware / Edge Readiness**: Highlight `esp32_dht11_oled.ino` and `simulator.py` demonstrating edge-to-cloud integration.
