#!/usr/bin/env python3
"""EnviroSense Edge Sensor Simulator.

Generates realistic environmental & air quality telemetry and publishes to:
- Amazon AWS API Gateway & DynamoDB Cloud
- Local EnviroSense Bridge Server (localhost:3000)

Supports operational modes: normal, heatwave, freeze, gasleak, and sinusoidal fluctuation.
"""

import argparse
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# Live Cloud & Local Default Endpoints
DEFAULT_AWS_API_URL = "https://etejnaemlc.execute-api.us-east-1.amazonaws.com/telemetry"
DEFAULT_LOCAL_API_URL = "http://localhost:3000/telemetry"


def compute_heat_index(temp_c: float, rh: float) -> float:
    """Calculate Steadman/Rothfusz Heat Index in Celsius."""
    t_f = (temp_c * 9.0 / 5.0) + 32.0
    hi_f = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh * 0.094))
    if hi_f >= 80.0:
        hi_f = (
            -42.379
            + (2.04901523 * t_f)
            + (10.14333127 * rh)
            - (0.22475541 * t_f * rh)
            - (0.00683783 * (t_f ** 2))
            - (0.05481717 * (rh ** 2))
            + (0.00122874 * (t_f ** 2) * rh)
            + (0.00085282 * t_f * (rh ** 2))
            - (0.00000199 * (t_f ** 2) * (rh ** 2))
        )
    return round((hi_f - 32.0) * 5.0 / 9.0, 2)


def generate_reading(mode: str, step: int) -> tuple[float, float, float]:
    """Return realistic (temperature_c, humidity_pct, gas_ppm) based on operational mode."""
    if mode == "gasleak":
        base_t = 26.5 + (random.uniform(-0.8, 1.2))
        base_h = 52.0 + (random.uniform(-3.0, 3.0))
        gas_ppm = round(random.uniform(680.0, 890.0), 1)
    elif mode == "heatwave":
        base_t = 41.5 + (random.uniform(-1.0, 1.8))
        base_h = 82.0 + (random.uniform(-4.0, 6.0))
        gas_ppm = round(random.uniform(220.0, 310.0), 1)
    elif mode == "freeze":
        base_t = 2.5 + (random.uniform(-1.5, 1.2))
        base_h = 32.0 + (random.uniform(-3.0, 4.0))
        gas_ppm = round(random.uniform(140.0, 190.0), 1)
    elif mode == "fluctuate":
        # Diurnal sine wave cycle
        cycle = math.sin(step * 0.1)
        base_t = 26.0 + (cycle * 9.0) + random.uniform(-0.5, 0.5)
        base_h = 55.0 - (cycle * 15.0) + random.uniform(-1.0, 1.0)
        gas_ppm = round(max(50.0, 180.0 + (cycle * 60.0) + random.uniform(-10.0, 10.0)), 1)
    else:  # normal
        base_t = 24.2 + random.uniform(-1.2, 1.2)
        base_h = 48.5 + random.uniform(-2.5, 2.5)
        gas_ppm = round(random.uniform(160.0, 210.0), 1)

    temp_c = round(max(-40.0, min(80.0, base_t)), 2)
    hum_pct = round(max(0.0, min(100.0, base_h)), 2)
    return temp_c, hum_pct, gas_ppm


def make_payload(args: argparse.Namespace, step: int) -> dict:
    temp_c, hum_pct, gas_ppm = generate_reading(args.mode, step)
    hi_c = compute_heat_index(temp_c, hum_pct)
    gas_raw = int(gas_ppm * 4.095)

    if gas_ppm >= 600.0:
        air_quality = "HAZARDOUS"
        status = "GAS_ALERT"
        status_detail = f"Hazardous gas concentration: {gas_ppm:.0f} PPM."
    elif temp_c <= 5.0:
        air_quality = "GOOD"
        status = "FREEZE_ALERT"
        status_detail = f"Freezing temperature warning: {temp_c}°C."
    elif temp_c >= 40.0 or hi_c >= 40.0:
        air_quality = "MODERATE"
        status = "HEAT_ALERT"
        status_detail = f"Critical heat index danger: {hi_c}°C."
    elif hum_pct >= 85.0:
        air_quality = "GOOD"
        status = "HIGH_HUMIDITY"
        status_detail = f"High relative humidity: {hum_pct}%."
    elif gas_ppm >= 350.0:
        air_quality = "MODERATE"
        status = "WARNING"
        status_detail = f"Elevated VOC / gas concentration: {gas_ppm:.0f} PPM."
    else:
        air_quality = "EXCELLENT" if gas_ppm < 200.0 else "GOOD"
        status = "NORMAL"
        status_detail = "Climate parameters are within optimal ranges."

    return {
        "deviceId": args.device_id,
        "location": args.location,
        "temperatureC": temp_c,
        "humidityPct": hum_pct,
        "heatIndexC": hi_c,
        "gasPpm": gas_ppm,
        "gasRaw": gas_raw,
        "airQuality": air_quality,
        "status": status,
        "statusDetail": status_detail,
        "recordedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def normalize_endpoint(url: str) -> str:
    """Ensure URL cleanly ends with /telemetry without duplicate trailing paths."""
    clean = url.strip().rstrip("/")
    if not clean.endswith("/telemetry"):
        clean = f"{clean}/telemetry"
    return clean


def is_local_bridge_running(port: int = 3000) -> bool:
    """Quick socket check to detect if local bridge is active."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


def resolve_api_urls(args: argparse.Namespace) -> list[str]:
    """Resolve one or more active ingestion endpoints based on CLI flags or auto-detection."""
    if args.api_url:
        return [normalize_endpoint(args.api_url)]

    if args.target == "both":
        return [DEFAULT_LOCAL_API_URL, DEFAULT_AWS_API_URL]

    if args.target == "local":
        return [DEFAULT_LOCAL_API_URL]

    if args.target == "aws":
        return [DEFAULT_AWS_API_URL]

    # Auto-detection: prefer local bridge if running (which automatically relays to AWS)
    if is_local_bridge_running(3000):
        return [DEFAULT_LOCAL_API_URL]
    return [DEFAULT_AWS_API_URL]


def publish(endpoint: str, payload: dict, api_key: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req, timeout=8) as resp:
        if resp.status >= 300:
            raise RuntimeError(f"API returned HTTP {resp.status}")
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def main() -> None:
    parser = argparse.ArgumentParser(description="EnviroSense IoT Sensor Telemetry Simulator")
    parser.add_argument(
        "--api-url",
        help="Target endpoint (defaults to live AWS API Gateway or local bridge)",
    )
    parser.add_argument(
        "--target",
        choices=["auto", "aws", "local", "both"],
        default="auto",
        help="Target destination: 'aws' (Live AWS API Gateway), 'local' (Local Bridge), 'both' (Dual publish), or 'auto' (detects active server)",
    )
    parser.add_argument("--api-key", help="API Gateway x-api-key header (optional)")
    parser.add_argument("--device-id", default="enviro-sim-01", help="Device identifier")
    parser.add_argument("--location", default="Campus Greenhouse Lab", help="Physical location label")
    parser.add_argument("--interval", type=float, default=3.0, help="Seconds between telemetry posts (default: 3.0s)")
    parser.add_argument(
        "--mode",
        choices=["normal", "heatwave", "freeze", "fluctuate", "gasleak"],
        default="normal",
        help="Telemetry simulation pattern (default: normal)",
    )
    parser.add_argument("--once", action="store_true", help="Send a single reading and terminate")
    parser.add_argument("--dry-run", action="store_true", help="Format and print JSON payload without sending")
    args = parser.parse_args()

    active_urls = resolve_api_urls(args)

    print("=======================================================================", flush=True)
    print("  EnviroSense — IoT Edge Sensor Node Simulator", flush=True)
    print(f"  Device: {args.device_id} | Location: {args.location}", flush=True)
    print(f"  Mode:   {args.mode.upper()} | Interval: {args.interval}s", flush=True)
    if args.dry_run:
        print("  Target: DRY-RUN (Local JSON preview only, no network calls)", flush=True)
    else:
        print(f"  Target: {', '.join(active_urls)}", flush=True)
    print("=======================================================================\n", flush=True)

    step = 0
    try:
        while True:
            payload = make_payload(args, step)
            now_str = datetime.now().strftime("%H:%M:%S")
            print(f"[{now_str}] Sensor Reading:")
            print(
                f"  Temp: {payload['temperatureC']} °C | Hum: {payload['humidityPct']} % | "
                f"Heat Index: {payload['heatIndexC']} °C | Gas: {payload['gasPpm']} PPM ({payload['airQuality']}) -> Status: {payload['status']}"
            )

            if args.dry_run:
                print(f"  [DRY-RUN JSON] {json.dumps(payload)}\n", flush=True)
            else:
                for target_url in active_urls:
                    try:
                        res = publish(target_url, payload, args.api_key)
                        dest_label = "AWS DynamoDB Cloud" if "amazonaws.com" in target_url else "Local Bridge"
                        print(f"  [HTTP 201 OK] Telemetry accepted by {dest_label} ({res.get('message', 'Recorded')})", flush=True)
                    except Exception as err:
                        print(f"  [HTTP ERROR] Failed to send to {target_url}: {err}", flush=True)
                print("", flush=True)

            if args.once:
                break

            step += 1
            time.sleep(max(0.5, args.interval))
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")


if __name__ == "__main__":
    main()
