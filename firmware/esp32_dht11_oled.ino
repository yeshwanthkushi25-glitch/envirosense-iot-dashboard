/*
 * EnviroSense — ESP32 + DHT11/DHT22 + SSD1306 OLED IoT Node
 * Course: Cloud Computing (25CAI102PC205) · Product #23 · SR University
 * 
 * Hardware Required:
 * 1. ESP32 DevKit V1 (30-pin or 38-pin)
 * 2. DHT11 or DHT22 Temperature & Humidity Sensor
 * 3. SSD1306 0.96" I2C OLED Display (128x64)
 * 4. Breadboard & Jumper wires
 * 
 * Libraries Required (install via Arduino Library Manager):
 * - "DHT sensor library" by Adafruit (and Adafruit Unified Sensor)
 * - "Adafruit SSD1306" by Adafruit
 * - "Adafruit GFX Library" by Adafruit
 * - "ArduinoJson" by Benoit Blanchon (version 6 or 7)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ================= CONFIGURATION =================
// 1. Wi-Fi Credentials
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// 2. AWS API Gateway Endpoint
// Replace with the StatusApiUrl / EnviroApiUrl output from your CloudFormation / SAM deployment
const char* API_URL       = "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/telemetry";
const char* API_KEY       = ""; // Leave empty if no API key is required

// 3. Hardware Pin Definitions
#define DHTPIN       4        // ESP32 GPIO 4 connected to DHT11 DATA pin
#define DHTTYPE      DHT11    // Change to DHT22 if using white sensor
#define OLED_SDA     21       // ESP32 GPIO 21 -> OLED SDA
#define OLED_SCL     22       // ESP32 GPIO 22 -> OLED SCL
#define OLED_RESET   -1       // Reset pin (-1 sharing Arduino reset)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// 4. Reporting Interval
const unsigned long REPORT_INTERVAL_MS = 6000; // 6 seconds

// Device Metadata
const char* DEVICE_ID = "enviro-esp32-01";
const char* LOCATION  = "Campus Greenhouse Lab";

// ================= OBJECT INSTANTIATION =================
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

unsigned long lastReportTime = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n--- EnviroSense ESP32 IoT Node Starting ---");

  // Initialize I2C and OLED
  Wire.begin(OLED_SDA, OLED_SCL);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed. Check wiring!"));
  } else {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(10, 10);
    display.println("EnviroSense ESP32");
    display.setCursor(10, 26);
    display.println("Connecting WiFi...");
    display.display();
  }

  // Initialize DHT sensor
  dht.begin();

  // Connect to Wi-Fi
  connectWiFi();
}

void loop() {
  // Reconnect Wi-Fi if connection drops
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastReportTime >= REPORT_INTERVAL_MS) {
    lastReportTime = currentMillis;

    // Read sensor
    float temperature = dht.readTemperature(); // Celsius
    float humidity    = dht.readHumidity();    // Relative %

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println(F("[ERROR] Failed to read from DHT sensor!"));
      updateOLEDError("Sensor Read Error");
      return;
    }

    // Compute Heat Index in Celsius
    float heatIndex = dht.computeHeatIndex(temperature, humidity, false);

    Serial.printf("[SENSOR] Temp: %.1f C | Hum: %.1f %% | Heat Index: %.1f C\n",
                  temperature, humidity, heatIndex);

    // Update OLED screen
    updateOLED(temperature, humidity, heatIndex);

    // Transmit telemetry to AWS
    sendTelemetryToAWS(temperature, humidity, heatIndex);
  }
}

void connectWiFi() {
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[OK] Wi-Fi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WARN] Wi-Fi connect timeout; will retry in loop.");
  }
}

void updateOLED(float temp, float hum, float hi) {
  display.clearDisplay();

  // Header Bar
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("EnviroSense");
  display.setCursor(76, 0);
  display.print(WiFi.status() == WL_CONNECTED ? "WiFi:OK" : "WiFi:--");
  display.drawLine(0, 10, 128, 10, SSD1306_WHITE);

  // Temperature
  display.setCursor(0, 16);
  display.print("Temp: ");
  display.setTextSize(2);
  display.print(temp, 1);
  display.setTextSize(1);
  display.print(" C");

  // Humidity
  display.setCursor(0, 36);
  display.print("Humidity: ");
  display.setTextSize(1);
  display.print(hum, 1);
  display.print(" %");

  // Heat Index
  display.setCursor(0, 48);
  display.print("Heat Index: ");
  display.print(hi, 1);
  display.print(" C");

  // Status indicator
  display.drawLine(0, 58, 128, 58, SSD1306_WHITE);
  display.setCursor(0, 56);
  if (temp >= 40.0) {
    display.print("ALERT: HEAT HAZARD!");
  } else if (temp <= 5.0) {
    display.print("ALERT: FREEZE HAZARD!");
  } else {
    display.print("STATUS: CLIMATE OK");
  }

  display.display();
}

void updateOLEDError(const char* message) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 20);
  display.println("SENSING WARNING");
  display.setCursor(10, 36);
  display.println(message);
  display.display();
}

void sendTelemetryToAWS(float temp, float hum, float hi) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[SKIP] WiFi not connected. Cannot publish.");
    return;
  }

  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");
  if (strlen(API_KEY) > 0) {
    http.addHeader("x-api-key", API_KEY);
  }

  // Construct JSON Document
  StaticJsonDocument<256> doc;
  doc["deviceId"]     = DEVICE_ID;
  doc["location"]     = LOCATION;
  doc["temperatureC"] = temp;
  doc["humidityPct"]  = hum;
  doc["heatIndexC"]   = hi;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  Serial.print("[HTTP] Publishing payload: ");
  Serial.println(jsonPayload);

  int httpResponseCode = http.POST(jsonPayload);
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.printf("[HTTP] Response Code %d: %s\n", httpResponseCode, response.c_str());
  } else {
    Serial.printf("[HTTP ERROR] Failed code: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();
}
