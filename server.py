"""EnviroSense Local Server & Wokwi IoT Gateway Bridge.

Course: Cloud Computing (25CAI102PC205) · Product #23 · SR University

Features:
1. Serves dashboard frontend assets (index.html, styles.css, app.js).
2. Telemetry Bridge API:
   - POST /telemetry: Receives live sensor readings from Wokwi ESP32 (via http://host.wokwi.internal:<port>/telemetry).
   - GET /telemetry: Delivers live readings and history to the web dashboard.
   - OPTIONS /telemetry: Handles CORS preflight.
"""

from datetime import datetime, timezone
import json
import mimetypes
import os
import sys
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(os.path.join(BASE_DIR, "frontend")):
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
elif os.path.isdir(os.path.join(BASE_DIR, "cloud computing product 2", "frontend")):
    FRONTEND_DIR = os.path.join(BASE_DIR, "cloud computing product 2", "frontend")
else:
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Live AWS API Gateway endpoint for cloud relay
AWS_API_GATEWAY_URL = os.environ.get(
    "AWS_API_GATEWAY_URL",
    "https://etejnaemlc.execute-api.us-east-1.amazonaws.com/telemetry"
)


def relay_to_aws(item: dict[str, Any]):
    """Asynchronously forward live ESP32 telemetry to AWS DynamoDB via API Gateway."""
    def _worker():
        try:
            import urllib.request
            payload = json.dumps(item).encode("utf-8")
            req = urllib.request.Request(
                AWS_API_GATEWAY_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in (200, 201):
                    print(f"  └─► [AWS DYNAMODB SYNC] Telemetry safely recorded in AWS Cloud ({resp.status})", flush=True)
                else:
                    print(f"  └─► [AWS DYNAMODB WARN] HTTP {resp.status}", flush=True)
        except Exception as e:
            print(f"  └─► [AWS SYNC NOTE] {e}", flush=True)
    import threading
    threading.Thread(target=_worker, daemon=True).start()

# In-memory telemetry buffer
MAX_HISTORY = 40
telemetry_history: list[dict[str, Any]] = [
    {
        "deviceId": "enviro-esp32-01",
        "location": "Campus Greenhouse Lab",
        "temperatureC": 24.5,
        "humidityPct": 48.0,
        "heatIndexC": 24.3,
        "gasPpm": 180.0,
        "airQuality": "GOOD",
        "status": "NORMAL",
        "statusDetail": "Climate & air quality parameters are optimal.",
        "recordedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "updatedAt": int(time.time()),
    }
]


def compute_heat_index(temp_c: float, rh: float) -> float:
    """Calculate apparent Heat Index in Celsius using the official NOAA NWS algorithm.
    
    Reference: National Oceanic and Atmospheric Administration (NOAA) /
    National Weather Service (NWS) Technical Attachment SR 90-23 (Rothfusz, 1990).
    """
    if temp_c <= 20.0:
        return round(temp_c, 1)

    t_f = (temp_c * 9.0 / 5.0) + 32.0
    rh_c = max(0.0, min(100.0, float(rh)))

    # Step 1: Steadman simple formula
    hi_simple = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh_c * 0.094))

    # Step 2: NOAA decision rule
    if (hi_simple + t_f) / 2.0 < 80.0:
        hi_f = hi_simple
    else:
        # Step 3: Full 9-term Rothfusz polynomial regression
        hi_f = (
            -42.379
            + (2.04901523 * t_f)
            + (10.14333127 * rh_c)
            - (0.22475541 * t_f * rh_c)
            - (0.00683783 * (t_f**2))
            - (0.05481717 * (rh_c**2))
            + (0.00122874 * (t_f**2) * rh_c)
            + (0.00085282 * t_f * (rh_c**2))
            - (0.00000199 * (t_f**2) * (rh_c**2))
        )

        # Step 4: NOAA Adjustment 1 (Low humidity: RH < 13% and 80 <= T <= 112 °F)
        if rh_c < 13.0 and 80.0 <= t_f <= 112.0:
            adj = ((13.0 - rh_c) / 4.0) * (((17.0 - abs(t_f - 95.0)) / 17.0) ** 0.5)
            hi_f -= adj

        # Step 5: NOAA Adjustment 2 (High humidity: RH > 85% and 80 <= T <= 87 °F)
        elif rh_c > 85.0 and 80.0 <= t_f <= 87.0:
            adj = ((rh_c - 85.0) / 10.0) * ((87.0 - t_f) / 5.0)
            hi_f += adj

    return round((hi_f - 32.0) * 5.0 / 9.0, 1)


def compute_aqi(gas_ppm: float) -> tuple[int, str]:
    """Calculate EPA-standard Air Quality Index (0-500) and category label from gas PPM."""
    g = max(0.0, float(gas_ppm))
    breakpoints = [
        (0.0, 200.0, 0, 50),        # Good (0-50)
        (201.0, 350.0, 51, 100),    # Moderate (51-100)
        (351.0, 500.0, 101, 150),   # Unhealthy for Sensitive Groups (101-150)
        (501.0, 650.0, 151, 200),   # Unhealthy (151-200)
        (601.0, 700.0, 201, 300),   # Very Unhealthy (201-300)
        (701.0, 1000.0, 301, 500),  # Hazardous (301-500)
    ]
    aqi = 500
    for c_low, c_high, i_low, i_high in breakpoints:
        if g <= c_high:
            if c_high == c_low:
                aqi = i_low
            else:
                aqi = round(((i_high - i_low) / (c_high - c_low)) * (g - c_low) + i_low)
            break
    aqi = max(0, min(500, aqi))

    if aqi <= 50:
        category = "GOOD"
    elif aqi <= 100:
        category = "MODERATE"
    elif aqi <= 150:
        category = "UNHEALTHY (USG)"
    elif aqi <= 200:
        category = "UNHEALTHY"
    elif aqi <= 300:
        category = "VERY UNHEALTHY"
    else:
        category = "HAZARDOUS"
    return aqi, category


def evaluate_status(
    temp_c: float, hum: float, hi: float, gas_ppm: float
) -> tuple[str, str]:
    if gas_ppm >= 600.0:
        return (
            "GAS_ALERT",
            f"Hazardous gas / air pollution alert: {gas_ppm:.0f} PPM detected by MQ-135!",
        )
    if temp_c >= 40.0 or hi >= 40.0:
        return "HEAT_ALERT", f"Critical thermal danger: Heat index is {hi:.1f}°C."
    if temp_c <= 5.0:
        return "FREEZE_ALERT", f"Freezing frost hazard: {temp_c:.1f}°C detected."
    if hum >= 85.0:
        return "HIGH_HUMIDITY", f"High relative humidity warning: {hum:.1f}%."
    if gas_ppm >= 350.0:
        return "WARNING", f"Elevated VOC/gas levels: {gas_ppm:.0f} PPM."
    return "NORMAL", "Climate & air quality parameters are optimal."


class EnviroSenseBridgeHandler(SimpleHTTPRequestHandler):

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD"
        )
        self.send_header(
            "Access-Control-Allow-Headers", "Content-Type, x-api-key"
        )

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        # 1. Telemetry API endpoint
        if path == "/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()

            payload = {
                "count": len(telemetry_history),
                "latest": telemetry_history[-1] if telemetry_history else None,
                "telemetry": list(reversed(telemetry_history)),
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        # 2. Frontend static files
        if path == "/" or path == "":
            file_path = os.path.join(FRONTEND_DIR, "index.html")
        else:
            rel_path = path.lstrip("/")
            file_path = os.path.join(FRONTEND_DIR, rel_path)

        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Server error: {e}".encode("utf-8"))
        else:
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        path = self.path.split("?")[0]
        if path != "/telemetry":
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": f"Invalid JSON: {e}"}).encode("utf-8")
            )
            return

        # Extract & validate fields
        device_id = str(data.get("deviceId", "enviro-esp32-01"))
        location = str(data.get("location", "Campus Greenhouse Lab"))
        temp_c = float(data.get("temperatureC", 24.0))
        hum = float(data.get("humidityPct", 50.0))
        gas_ppm = float(data.get("gasPpm", 150.0))

        hi = (
            float(data["heatIndexC"])
            if "heatIndexC" in data
            else compute_heat_index(temp_c, hum)
        )
        status = data.get("status")
        if not status:
            status, status_detail = evaluate_status(temp_c, hum, hi, gas_ppm)
        else:
            _, status_detail = evaluate_status(temp_c, hum, hi, gas_ppm)

        calc_aqi, calc_category = compute_aqi(gas_ppm)
        aqi_val = int(data.get("aqi", calc_aqi))
        air_quality = str(data.get("airQuality", "")).strip() or calc_category

        now_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        now_ts = int(time.time())

        item = {
            "deviceId": device_id,
            "location": location,
            "temperatureC": round(temp_c, 1),
            "humidityPct": round(hum, 1),
            "heatIndexC": round(hi, 1),
            "gasPpm": round(gas_ppm),
            "aqi": aqi_val,
            "airQuality": air_quality,
            "status": status,
            "statusDetail": status_detail,
            "recordedAt": now_utc,
            "updatedAt": now_ts,
        }

        telemetry_history.append(item)
        if len(telemetry_history) > MAX_HISTORY:
            telemetry_history.pop(0)

        # Print log to terminal
        print(
            f"[ESP32 -> BRIDGE] Temp: {item['temperatureC']}°C | Hum: "
            f"{item['humidityPct']}% | HeatIdx: {item['heatIndexC']}°C | "
            f"AQI: {item['aqi']} ({item['airQuality']}, {item['gasPpm']} PPM) -> {item['status']}"
        )

        # Asynchronously synchronize with AWS DynamoDB
        relay_to_aws(item)

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(
            json.dumps({"message": "Telemetry recorded", "telemetry": item}).encode(
                "utf-8"
            )
        )


def run_server(port: int = 3000):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, EnviroSenseBridgeHandler)
    print("=" * 65)
    print(
        f"  EnviroSense Bridge Server running on http://localhost:{port} (0.0.0.0)"
    )
    print("  Serving frontend dashboard & receiving live Wokwi ESP32 telemetry")
    print(
        f"  Virtual ESP32 Wokwi Endpoint: http://host.wokwi.internal:{port}/telemetry"
    )
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    run_server(port_arg)
