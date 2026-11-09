"""EnviroSense IoT Environmental Telemetry & Climate Dashboard Lambda handler."""

import base64
import json
import math
import os
import time
from datetime import datetime, timezone
from typing import Any

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "envirosense-telemetry-local")
TTL_SECONDS = int(os.environ.get("TELEMETRY_TTL_SECONDS", "86400"))
table = boto3.resource("dynamodb").Table(TABLE_NAME)

MAX_DEVICE_ID_LENGTH = 80
MAX_LOCATION_LENGTH = 120

# Environmental Thresholds
TEMP_FREEZE_THRESHOLD = 5.0      # <= 5.0 °C
TEMP_HEAT_WARNING = 35.0         # >= 35.0 °C
TEMP_HEAT_DANGER = 40.0          # >= 40.0 °C
HUMIDITY_HIGH_WARNING = 80.0     # >= 80.0 %


def response(status_code: int, body: Any) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "content-type,x-api-key",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(body),
    }


def parse_body(event: dict[str, Any]) -> dict[str, Any]:
    raw_body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw_body = base64.b64decode(raw_body).decode("utf-8")
    if isinstance(raw_body, dict):
        return raw_body
    parsed = json.loads(raw_body)
    if not isinstance(parsed, dict):
        raise ValueError("Request body must be a JSON object")
    return parsed


def compute_heat_index(temp_c: float, humidity_pct: float) -> float:
    """Calculate Steadman/Rothfusz Heat Index in Celsius."""
    # Convert Celsius to Fahrenheit for empirical formula
    t_f = (temp_c * 9.0 / 5.0) + 32.0
    rh = humidity_pct

    # Simple formula below 80°F (approx 26.7°C)
    hi_f = 0.5 * (t_f + 61.0 + ((t_f - 68.0) * 1.2) + (rh * 0.094))

    # Full Rothfusz regression if warm enough
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

    # Convert back to Celsius
    hi_c = (hi_f - 32.0) * 5.0 / 9.0
    return round(hi_c, 2)


def evaluate_status(temp_c: float, humidity_pct: float, heat_index_c: float) -> tuple[str, str]:
    """Return status category and descriptive message."""
    if temp_c <= TEMP_FREEZE_THRESHOLD:
        return "FREEZE_ALERT", f"Low temperature warning: {temp_c}°C detected."
    if temp_c >= TEMP_HEAT_DANGER or heat_index_c >= TEMP_HEAT_DANGER:
        return "HEAT_ALERT", f"Critical heat index danger: {heat_index_c}°C."
    if temp_c >= TEMP_HEAT_WARNING:
        return "WARNING", f"Elevated temperature detected: {temp_c}°C."
    if humidity_pct >= HUMIDITY_HIGH_WARNING:
        return "HIGH_HUMIDITY", f"High relative humidity: {humidity_pct}%."
    return "NORMAL", "Climate parameters are within optimal ranges."


def validate_telemetry(payload: dict[str, Any]) -> dict[str, Any]:
    device_id = str(payload.get("deviceId", "enviro-node-01")).strip()
    if not device_id or len(device_id) > MAX_DEVICE_ID_LENGTH:
        raise ValueError("deviceId is required and must be 80 characters or fewer")

    location = str(payload.get("location", "Campus Lab 102")).strip() or "Campus Lab 102"
    location = location[:MAX_LOCATION_LENGTH]

    # Temperature validation (-40°C to +85°C valid operational range for sensors)
    try:
        temp_c = round(float(payload["temperatureC"]), 2)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("temperatureC is required and must be a valid number") from exc

    if temp_c < -40.0 or temp_c > 85.0:
        raise ValueError("temperatureC must be between -40.0°C and 85.0°C")

    # Humidity validation (0% to 100%)
    try:
        humidity_pct = round(float(payload["humidityPct"]), 2)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("humidityPct is required and must be a valid number") from exc

    if humidity_pct < 0.0 or humidity_pct > 100.0:
        raise ValueError("humidityPct must be between 0.0% and 100.0%")

    # Optional heat index or compute dynamically
    if "heatIndexC" in payload and payload["heatIndexC"] is not None:
        try:
            heat_index_c = round(float(payload["heatIndexC"]), 2)
        except (TypeError, ValueError):
            heat_index_c = compute_heat_index(temp_c, humidity_pct)
    else:
        heat_index_c = compute_heat_index(temp_c, humidity_pct)

    status, status_detail = evaluate_status(temp_c, humidity_pct, heat_index_c)

    # Timestamp handling
    recorded_at = str(payload.get("recordedAt", "")).strip()
    if recorded_at:
        try:
            datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("recordedAt must be a valid ISO-8601 timestamp") from exc
    else:
        recorded_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    now = int(time.time())
    item = {
        "deviceId": device_id,
        "recordedAt": recorded_at,
        "location": location,
        "temperatureC": temp_c,
        "humidityPct": humidity_pct,
        "heatIndexC": heat_index_c,
        "status": status,
        "statusDetail": status_detail,
        "updatedAt": now,
        "expiresAt": now + TTL_SECONDS,
    }
    return item


def handle_post(event: dict[str, Any]) -> dict[str, Any]:
    try:
        item = validate_telemetry(parse_body(event))
    except (ValueError, json.JSONDecodeError) as exc:
        return response(400, {"error": str(exc)})

    table.put_item(Item=item)
    return response(201, {"message": "Telemetry recorded", "telemetry": item})


def handle_get(event: dict[str, Any]) -> dict[str, Any]:
    query = event.get("queryStringParameters") or {}
    device_id = (query.get("deviceId") or "").strip()
    limit = query.get("limit")

    if device_id:
        # Query specific device
        result = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("deviceId").eq(device_id),
            ScanIndexForward=False,
            Limit=int(limit) if limit and limit.isdigit() else 20,
        ) if hasattr(boto3, "dynamodb") and hasattr(boto3.dynamodb, "conditions") else table.scan()
        items = result.get("Items", [])
        if not items:
            return response(404, {"error": f"No telemetry found for device: {device_id}"})
        return response(200, {"deviceId": device_id, "latest": items[0], "history": items})

    # Default scan to return all recent device telemetry
    result = table.scan()
    items = sorted(result.get("Items", []), key=lambda x: x.get("updatedAt", 0), reverse=True)
    return response(200, {
        "count": len(items),
        "latest": items[0] if items else None,
        "telemetry": items[:30],
    })


def handler(event: dict[str, Any], _context: Any) -> dict[str, Any]:
    """Dispatch API Gateway HTTP API events."""
    method = (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod", "")
    ).upper()

    try:
        if method == "POST":
            return handle_post(event)
        if method == "GET":
            return handle_get(event)
        if method == "OPTIONS":
            return response(204, {})
        return response(405, {"error": "Method not allowed"})
    except Exception:
        # Keep internal details out of the response; CloudWatch logs contain the stack trace
        print("Unhandled EnviroSense API error", flush=True)
        raise
