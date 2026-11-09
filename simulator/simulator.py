#!/usr/bin/env python3
"""EnviroSense Edge Sensor Simulator.

Generates realistic environmental sensor telemetry and publishes to the AWS API Gateway.
Supports multiple operational modes: normal, heatwave, freeze, and sinusoidal fluctuation.
"""

import argparse
import json
import math
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


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


def generate_reading(mode: str, step: int) -> tuple[float, float]:
    """Return realistic (temperature_c, humidity_pct) based on operational mode."""
    if mode == "heatwave":
        base_t = 41.5 + (random.uniform(-1.0, 1.8))
        base_h = 82.0 + (random.uniform(-4.0, 6.0))
    elif mode == "freeze":
        base_t = 2.5 + (random.uniform(-1.5, 1.2))
        base_h = 32.0 + (random.uniform(-3.0, 4.0))
    elif mode == "fluctuate":
        # Diurnal sine wave cycle
        cycle = math.sin(step * 0.1)
        base_t = 26.0 + (cycle * 9.0) + random.uniform(-0.5, 0.5)
        base_h = 55.0 - (cycle * 15.0) + random.uniform(-1.0, 1.0)
    else:  # normal
        base_t = 24.2 + random.uniform(-1.2, 1.2)
        base_h = 48.5 + random.uniform(-2.5, 2.5)

    temp_c = round(max(-40.0, min(80.0, base_t)), 2)
    hum_pct = round(max(0.0, min(100.0, base_h)), 2)
    return temp_c, hum_pct


def make_payload(args: argparse.Namespace, step: int) -> dict:
    temp_c, hum_pct = generate_reading(args.mode, step)
    hi_c = compute_heat_index(temp_c, hum_pct)

    return {
        "deviceId": args.device_id,
        "location": args.location,
        "temperatureC": temp_c,
        "humidityPct": hum_pct,
        "heatIndexC": hi_c,
        "recordedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def publish(api_url: str, payload: dict, api_key: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    endpoint = f"{api_url.rstrip('/')}/telemetry"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req, timeout=10) as resp:
        if resp.status >= 300:
            raise RuntimeError(f"API returned HTTP {resp.status}")
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def main() -> None:
    parser = argparse.ArgumentParser(description="EnviroSense IoT Sensor Telemetry Simulator")
    parser.add_argument("--api-url", help="API Gateway URL (required unless --dry-run is set)")
    parser.add_argument("--api-key", help="API Gateway x-api-key header")
    parser.add_argument("--device-id", default="enviro-node-01", help="Device identifier")
    parser.add_argument("--location", default="Campus Greenhouse Lab", help="Physical location label")
    parser.add_argument("--interval", type=float, default=5.0, help="Seconds between telemetry posts")
    parser.add_argument("--mode", choices=["normal", "heatwave", "freeze", "fluctuate"], default="normal",
                        help="Telemetry simulation pattern")
    parser.add_argument("--once", action="store_true", help="Send a single reading and terminate")
    parser.add_argument("--dry-run", action="store_true", help="Format and print JSON payload without sending")
    args = parser.parse_args()

    if not args.api_url and not args.dry_run:
        parser.error("--api-url is required unless --dry-run is specified")

    print("=======================================================", flush=True)
    print("  EnviroSense — IoT Edge Sensor Node Simulator", flush=True)
    print(f"  Device: {args.device_id} | Location: {args.location}", flush=True)
    print(f"  Mode: {args.mode.upper()} | Interval: {args.interval}s", flush=True)
    print("=======================================================\n", flush=True)

    step = 0
    try:
        while True:
            payload = make_payload(args, step)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Telemetry payload:")
            print(f"  Temperature: {payload['temperatureC']} °C | Humidity: {payload['humidityPct']} % | Heat Index: {payload['heatIndexC']} °C")

            if args.dry_run:
                print(f"  [DRY-RUN JSON] {json.dumps(payload)}\n")
            elif args.api_url:
                try:
                    res = publish(args.api_url, payload, args.api_key)
                    print(f"  [HTTP 201 OK] Telemetry published -> DynamoDB: {res.get('message')}\n", flush=True)
                except Exception as err:
                    print(f"  [HTTP ERROR] Failed to send: {err}\n", flush=True)

            if args.once:
                break

            step += 1
            time.sleep(max(0.5, args.interval))
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")


if __name__ == "__main__":
    main()
