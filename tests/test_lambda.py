import json
import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Mock boto3 DynamoDB resource so tests can run cleanly on any workstation without AWS credentials
sys.modules.setdefault("boto3", SimpleNamespace(
    resource=lambda *_args, **_kwargs: MagicMock(),
    dynamodb=SimpleNamespace(conditions=SimpleNamespace(Key=lambda x: MagicMock()))
))
import app  # noqa: E402


class EnviroSenseLambdaTests(unittest.TestCase):
    def setUp(self):
        self.table = MagicMock()
        self.table.scan.return_value = {"Items": []}

    def test_post_validates_and_stores_normal_telemetry(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({
                "deviceId": "enviro-node-01",
                "location": "Campus Greenhouse Lab",
                "temperatureC": 24.5,
                "humidityPct": 48.0,
            }),
        }
        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 201)
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "Telemetry recorded")

        stored = self.table.put_item.call_args.kwargs["Item"]
        self.assertEqual(stored["deviceId"], "enviro-node-01")
        self.assertEqual(stored["temperatureC"], 24.5)
        self.assertEqual(stored["humidityPct"], 48.0)
        self.assertEqual(stored["status"], "NORMAL")
        self.assertIn("heatIndexC", stored)
        self.assertIn("expiresAt", stored)

    def test_post_flags_heat_alert(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({
                "deviceId": "enviro-node-01",
                "temperatureC": 42.0,
                "humidityPct": 85.0,
            }),
        }
        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 201)
        stored = self.table.put_item.call_args.kwargs["Item"]
        self.assertEqual(stored["status"], "HEAT_ALERT")
        self.assertGreater(stored["heatIndexC"], 40.0)

    def test_post_flags_freeze_alert(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({
                "deviceId": "enviro-node-01",
                "temperatureC": 2.0,
                "humidityPct": 30.0,
            }),
        }
        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 201)
        stored = self.table.put_item.call_args.kwargs["Item"]
        self.assertEqual(stored["status"], "FREEZE_ALERT")

    def test_post_rejects_out_of_range_temperature(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({
                "deviceId": "enviro-node-01",
                "temperatureC": -95.0,  # Physically invalid for Earth/sensors
                "humidityPct": 50.0,
            }),
        }
        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 400)
        self.table.put_item.assert_not_called()

    def test_post_rejects_missing_humidity(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({
                "deviceId": "enviro-node-01",
                "temperatureC": 25.0,
            }),
        }
        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 400)
        self.table.put_item.assert_not_called()

    def test_get_returns_telemetry_list(self):
        mock_items = [
            {"deviceId": "enviro-node-01", "temperatureC": 24.5, "updatedAt": 100},
            {"deviceId": "enviro-node-02", "temperatureC": 22.1, "updatedAt": 90},
        ]
        self.table.scan.return_value = {"Items": mock_items}
        event = {"requestContext": {"http": {"method": "GET"}}, "queryStringParameters": None}

        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertEqual(body["count"], 2)
        self.assertEqual(body["latest"]["deviceId"], "enviro-node-01")

    def test_post_flags_gas_alert(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({
                "deviceId": "enviro-node-01",
                "temperatureC": 25.0,
                "humidityPct": 50.0,
                "gasPpm": 750.0,
            }),
        }
        with patch.object(app, "table", self.table):
            result = app.handler(event, None)

        self.assertEqual(result["statusCode"], 201)
        stored = self.table.put_item.call_args.kwargs["Item"]
        self.assertEqual(stored["status"], "GAS_ALERT")
        self.assertEqual(stored["airQuality"], "HAZARDOUS")
        self.assertEqual(stored["gasPpm"], 750.0)

    def test_noaa_heat_index_calculations(self):
        # 1. Cold conditions: Heat index equals ambient temperature (no heat fatigue)
        self.assertEqual(app.compute_heat_index(2.0, 40.0), 2.0)
        self.assertEqual(app.compute_heat_index(18.0, 60.0), 18.0)

        # 2. Moderate warmth (below 80°F avg): Steadman simple formula
        # 24.0°C (75.2°F), 50% RH -> simple formula
        hi_24 = app.compute_heat_index(24.0, 50.0)
        self.assertAlmostEqual(hi_24, 23.95, delta=0.5)

        # 3. Severe Heatwave: Rothfusz regression with high-humidity adjustment
        # 42.0°C (107.6°F), 85% RH -> critical heat index
        hi_hot = app.compute_heat_index(42.0, 85.0)
        self.assertGreater(hi_hot, 60.0)

    def test_epa_aqi_calculations(self):
        # 1. Clean ambient air (180 PPM) -> Good (AQI <= 50)
        aqi_good, cat_good = app.compute_aqi(180.0)
        self.assertEqual(cat_good, "GOOD")
        self.assertLessEqual(aqi_good, 50)

        # 2. Moderate pollution (280 PPM) -> Moderate (51-100)
        aqi_mod, cat_mod = app.compute_aqi(280.0)
        self.assertEqual(cat_mod, "MODERATE")
        self.assertTrue(51 <= aqi_mod <= 100)

        # 3. Toxic gas leak (750 PPM) -> Hazardous (301-500)
        aqi_haz, cat_haz = app.compute_aqi(750.0)
        self.assertEqual(cat_haz, "HAZARDOUS")
        self.assertTrue(301 <= aqi_haz <= 500)

    def test_options_cors_preflight(self):
        event = {"requestContext": {"http": {"method": "OPTIONS"}}}
        result = app.handler(event, None)
        self.assertEqual(result["statusCode"], 204)
        self.assertEqual(result["headers"]["Access-Control-Allow-Origin"], "*")
        self.assertIn("POST", result["headers"]["Access-Control-Allow-Methods"])


if __name__ == "__main__":
    unittest.main()
