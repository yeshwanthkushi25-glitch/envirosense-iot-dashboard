/*
 * EnviroSense — ESP32 + DHT22 + MQ-135 Gas Sensor + SSD1306 OLED IoT Node
 * Course: Cloud Computing (25CAI102PC205) · Product #23 · SR University
 * 
 * Hardware Connections:
 * 1. ESP32 DevKit V1 (30-pin / 38-pin)
 * 2. DHT22 Temperature & Humidity Sensor:
 *    - VCC  -> ESP32 3V3
 *    - GND  -> ESP32 GND
 *    - DATA -> ESP32 GPIO 4
 * 3. MQ-135 Air Quality / Gas Detection Sensor:
 *    - VCC  -> ESP32 3V3 / 5V
 *    - GND  -> ESP32 GND
 *    - AOUT -> ESP32 GPIO 34 (ADC1_CH6 - safe with WiFi)
 * 4. SSD1306 0.96" I2C OLED Display:
 *    - VCC  -> ESP32 3V3
 *    - GND  -> ESP32 GND
 *    - SDA  -> ESP32 GPIO 21
 *    - SCL  -> ESP32 GPIO 22
 * 
 * Simulation: Wokwi for VS Code (open diagram.json and run)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ================= CONFIGURATION & MODE TOGGLE =================
// 1 = Wokwi VS Code Simulator (Uses virtual Wokwi-GUEST WiFi & host.wokwi.internal bridge)
// 0 = Physical Hardware / Live AWS Deployment
#define USE_WOKWI_SIMULATION 1

#if USE_WOKWI_SIMULATION
  const char* WIFI_SSID     = "Wokwi-GUEST";
  const char* WIFI_PASSWORD = "";
  const int   WIFI_CHANNEL  = 6; // Fast-track channel for Wokwi virtual router
  const char* API_URL       = "http://host.wokwi.internal:3000/telemetry";
  const char* API_KEY       = "";
#else
  const char* WIFI_SSID     = "YOUR_WIFI_SSID";
  const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
  const int   WIFI_CHANNEL  = 0;
  const char* API_URL       = "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/telemetry";
  const char* API_KEY       = "";
#endif

// ================= HARDWARE PIN DEFINITIONS =================
#define DHTPIN       4
#define DHTTYPE      DHT22

#define MQ135_ANALOG_PIN  34    // GPIO 34 (ADC1)
#define MQ135_DIGITAL_PIN 35    // GPIO 35 (Optional)

#define OLED_SDA     21
#define OLED_SCL     22
#define OLED_RESET   -1
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

const char* DEVICE_ID = "enviro-esp32-01";
const char* LOCATION  = "Campus Greenhouse Lab";
const unsigned long REPORT_INTERVAL_MS = 5000;

DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

unsigned long lastReportTime = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n--- EnviroSense ESP32 IoT Node Starting (DHT22 + MQ135) ---");

  pinMode(MQ135_ANALOG_PIN, INPUT);

  Wire.begin(OLED_SDA, OLED_SCL);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("[WARN] SSD1306 OLED allocation failed."));
  } else {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(8, 10);
    display.println("EnviroSense Node");
    display.setCursor(8, 24);
    display.println("DHT22 + MQ-135 Gas");
    display.setCursor(8, 40);
    display.println(USE_WOKWI_SIMULATION ? "Wokwi Sim Starting..." : "WiFi Connecting...");
    display.display();
  }

  dht.begin();
  connectWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastReportTime >= REPORT_INTERVAL_MS) {
    lastReportTime = currentMillis;

    float temperature = dht.readTemperature();
    float humidity    = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println(F("[ERROR] Failed to read from DHT22 sensor!"));
      updateOLEDError("DHT22 Read Fault");
      return;
    }

    float heatIndex = dht.computeHeatIndex(temperature, humidity, false);

    int rawGasAdc = analogRead(MQ135_ANALOG_PIN);
    float gasPpm = readGasPpm(rawGasAdc);
    const char* airQuality = evaluateAirQuality(gasPpm);
    const char* overallStatus = evaluateOverallStatus(temperature, humidity, heatIndex, gasPpm);

    Serial.printf("[TELEMETRY] Temp: %.1f C | Hum: %.1f %% | HeatIdx: %.1f C | Gas: %.0f PPM [%s] -> %s\n",
                  temperature, humidity, heatIndex, gasPpm, airQuality, overallStatus);

    updateOLED(temperature, humidity, heatIndex, gasPpm, airQuality, overallStatus);
    sendTelemetry(temperature, humidity, heatIndex, gasPpm, airQuality, overallStatus);
  }
}

void connectWiFi() {
  Serial.printf("[WIFI] Connecting to SSID: '%s'...\n", WIFI_SSID);
  WiFi.mode(WIFI_STA);

  #if USE_WOKWI_SIMULATION
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD, WIFI_CHANNEL);
  #else
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  #endif

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 25) {
    delay(400);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI OK] Connected!");
    Serial.print("[WIFI OK] IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WIFI WARN] Timeout; will retry in loop.");
  }
}

float readGasPpm(int rawAdc) {
  float ppm = ((float)rawAdc / 4095.0f) * 1000.0f;
  if (ppm < 50.0f) ppm = 50.0f;
  return ppm;
}

const char* evaluateAirQuality(float gasPpm) {
  if (gasPpm >= 600.0f) return "HAZARDOUS";
  if (gasPpm >= 350.0f) return "MODERATE";
  if (gasPpm >= 200.0f) return "GOOD";
  return "EXCELLENT";
}

const char* evaluateOverallStatus(float temp, float hum, float hi, float gasPpm) {
  if (gasPpm >= 600.0f) return "GAS_ALERT";
  if (temp >= 40.0f || hi >= 40.0f) return "HEAT_ALERT";
  if (temp <= 5.0f) return "FREEZE_ALERT";
  if (hum >= 85.0f) return "HIGH_HUMIDITY";
  if (gasPpm >= 350.0f) return "WARNING";
  return "NORMAL";
}

void updateOLED(float temp, float hum, float hi, float gasPpm, const char* airQuality, const char* overallStatus) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("EnviroSense");
  display.setCursor(76, 0);
  display.print(WiFi.status() == WL_CONNECTED ? "WiFi:OK" : "WiFi:--");
  display.drawLine(0, 10, 128, 10, SSD1306_WHITE);

  display.setCursor(0, 14);
  display.printf("T:%.1fC  H:%.0f%%", temp, hum);

  display.setCursor(0, 26);
  display.printf("HI:%.1fC Gas:%.0f", hi, gasPpm);

  display.setCursor(0, 38);
  display.printf("Air: %s", airQuality);

  display.drawLine(0, 50, 128, 50, SSD1306_WHITE);
  display.setCursor(0, 54);
  if (strcmp(overallStatus, "GAS_ALERT") == 0) {
    display.print("ALERT: GAS LEAK!");
  } else if (strcmp(overallStatus, "HEAT_ALERT") == 0) {
    display.print("ALERT: HEAT HAZARD!");
  } else if (strcmp(overallStatus, "FREEZE_ALERT") == 0) {
    display.print("ALERT: FREEZE RISK!");
  } else if (strcmp(overallStatus, "HIGH_HUMIDITY") == 0) {
    display.print("WARN: HIGH HUMIDITY");
  } else {
    display.print("STATUS: OPTIMAL OK");
  }

  display.display();
}

void updateOLEDError(const char* message) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(8, 16);
  display.println("ENVIROSENSE FAULT");
  display.drawLine(0, 28, 128, 28, SSD1306_WHITE);
  display.setCursor(8, 36);
  display.println(message);
  display.display();
}

void sendTelemetry(float temp, float hum, float hi, float gasPpm, const char* airQuality, const char* overallStatus) {
  if (WiFi.status() != WL_CONNECTED) {
    return;
  }

  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");
  if (strlen(API_KEY) > 0) {
    http.addHeader("x-api-key", API_KEY);
  }

  StaticJsonDocument<384> doc;
  doc["deviceId"]     = DEVICE_ID;
  doc["location"]     = LOCATION;
  doc["temperatureC"] = round(temp * 10.0f) / 10.0f;
  doc["humidityPct"]  = round(hum * 10.0f) / 10.0f;
  doc["heatIndexC"]   = round(hi * 10.0f) / 10.0f;
  doc["gasPpm"]       = round(gasPpm);
  doc["airQuality"]   = airQuality;
  doc["status"]       = overallStatus;

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  int httpCode = http.POST(jsonPayload);
  if (httpCode > 0) {
    String response = http.getString();
    Serial.printf("[HTTP RES] %d: %s\n", httpCode, response.c_str());
  } else {
    Serial.printf("[HTTP ERR] Code: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}
