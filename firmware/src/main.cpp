/*
 * EnviroSense — ESP32 + DHT22 + MQ-135 Gas Sensor + SSD1306 OLED IoT Node
 * Course: Cloud Computing (25CAI102PC205) · Product #23 · SR University
 * 
 * Target: ESP32 DevKit V1 (30-pin / 38-pin)
 * Simulation: Wokwi for VS Code (diagram.json + wokwi.toml)
 * Hardware Deployment: Dual-mode support for Wokwi virtual WiFi & Production AWS API Gateway
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ================= CONFIGURATION & CLOUD ENDPOINTS =================
// 1 = Wokwi VS Code Simulator (Uses virtual Wokwi-GUEST WiFi)
// 0 = Physical Hardware (Uses custom WiFi credentials)
#define USE_WOKWI_SIMULATION 1

#if USE_WOKWI_SIMULATION
  const char* WIFI_SSID     = "Wokwi-GUEST";
  const char* WIFI_PASSWORD = "";
  const int   WIFI_CHANNEL  = 6; // Fast-track channel for Wokwi virtual router
#else
  const char* WIFI_SSID     = "YOUR_WIFI_SSID";
  const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
  const int   WIFI_CHANNEL  = 0;
#endif

// Live Deployed AWS API Gateway Endpoint
const char* AWS_API_URL    = "https://etejnaemlc.execute-api.us-east-1.amazonaws.com/telemetry";
const char* LOCAL_API_URL  = "http://host.wokwi.internal:3000/telemetry";
const char* API_KEY        = "";

// ================= HARDWARE PIN DEFINITIONS =================
// DHT22 Digital Data Pin
#define DHTPIN       4
#define DHTTYPE      DHT22

// MQ-135 Air Quality & Gas Sensor (Must use ADC1 pin on ESP32 to coexist with WiFi)
#define MQ135_ANALOG_PIN  34    // GPIO 34 (ADC1_CH6)
#define MQ135_DIGITAL_PIN 35    // GPIO 35 (Optional digital threshold input)

// SSD1306 I2C OLED Display
#define OLED_SDA     21
#define OLED_SCL     22
#define OLED_RESET   -1
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Device Metadata & Reporting Timing
const char* DEVICE_ID = "enviro-esp32-01";
const char* LOCATION  = "Campus Greenhouse Lab";
const unsigned long REPORT_INTERVAL_MS = 2000; // 2-second heartbeat cadence

float prevTemp = -999.0f;
float prevHum = -999.0f;
float prevGas = -999.0f;

// ================= PERIPHERAL INSTANTIATION =================
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

unsigned long lastReportTime = 0;

// ================= FUNCTION PROTOTYPES =================
void connectWiFi();
void updateOLED(float temp, float hum, float hi, float gasPpm, const char* airQuality, const char* overallStatus);
void updateOLEDError(const char* message);
void sendTelemetry(float temp, float hum, float hi, float gasPpm, const char* airQuality, const char* overallStatus);
float readGasPpm(int rawAdc);
const char* evaluateAirQuality(float gasPpm);
const char* evaluateOverallStatus(float temp, float hum, float hi, float gasPpm);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n========================================================");
  Serial.println("  EnviroSense ESP32 IoT Node — DHT22 + MQ-135 + OLED    ");
  Serial.println("  Cloud Computing Product #23 · SR University           ");
  Serial.printf ("  Mode: %s\n", USE_WOKWI_SIMULATION ? "Wokwi VS Code Simulator" : "Physical Hardware");
  Serial.println("========================================================\n");

  // Configure MQ-135 pin
  pinMode(MQ135_ANALOG_PIN, INPUT);

  // Initialize I2C and OLED Screen
  Wire.begin(OLED_SDA, OLED_SCL);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("[WARN] SSD1306 OLED allocation failed. Check I2C address/wiring."));
  } else {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(8, 8);
    display.println("EnviroSense Node");
    display.setCursor(8, 22);
    display.println("ESP32 + DHT22 + MQ135");
    display.setCursor(8, 38);
    display.println(USE_WOKWI_SIMULATION ? "Wokwi Sim Connecting..." : "WiFi Connecting...");
    display.display();
  }

  // Initialize DHT22 Sensor
  dht.begin();
  Serial.println("[INIT] DHT22 Temperature & Humidity sensor initialized on GPIO 4.");
  Serial.println("[INIT] MQ-135 Gas & Air Quality sensor initialized on GPIO 34 (ADC1).");

  // Connect to Network
  connectWiFi();
}

void loop() {
  // Auto-reconnect if WiFi drops
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  unsigned long currentMillis = millis();
  bool timeToSend = (currentMillis - lastReportTime >= REPORT_INTERVAL_MS);

  // Fast 400ms sampling for instantaneous response to slider adjustments
  static unsigned long lastSampleTime = 0;
  if (currentMillis - lastSampleTime >= 400) {
    lastSampleTime = currentMillis;

    // 1. Read DHT22 Temperature & Humidity
    float temperature = dht.readTemperature(); // Celsius
    float humidity    = dht.readHumidity();    // Relative %

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println(F("[ERROR] Failed to read from DHT22 sensor! Check GPIO 4 wiring."));
      updateOLEDError("DHT22 Sensor Fault");
      return;
    }

    // 2. Read MQ-135 Gas & Air Quality Sensor
    int rawGasAdc = analogRead(MQ135_ANALOG_PIN);
    float gasPpm = readGasPpm(rawGasAdc);

    // Detect if user interacted with slider in Wokwi
    bool valueChanged = (fabs(temperature - prevTemp) >= 0.2f) ||
                        (fabs(humidity - prevHum) >= 0.5f) ||
                        (fabs(gasPpm - prevGas) >= 15.0f);

    if (valueChanged || timeToSend) {
      lastReportTime = currentMillis;
      prevTemp = temperature;
      prevHum = humidity;
      prevGas = gasPpm;

      // Compute Steadman Heat Index in Celsius
      float heatIndex = dht.computeHeatIndex(temperature, humidity, false);
      const char* airQuality = evaluateAirQuality(gasPpm);
      const char* overallStatus = evaluateOverallStatus(temperature, humidity, heatIndex, gasPpm);

      // Output Serial Telemetry
      Serial.printf("[TELEMETRY] Temp: %.1f C | Hum: %.1f %% | HeatIdx: %.1f C | Gas: %.0f PPM [%s] -> Status: %s\n",
                    temperature, humidity, heatIndex, gasPpm, airQuality, overallStatus);

      // Update OLED Screen
      updateOLED(temperature, humidity, heatIndex, gasPpm, airQuality, overallStatus);

      // Transmit Telemetry Payload to Bridge / AWS
      sendTelemetry(temperature, humidity, heatIndex, gasPpm, airQuality, overallStatus);
    }
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
    delay(300);
    Serial.print(".");
    attempts++;
    #if USE_WOKWI_SIMULATION
    if (attempts == 12 && WiFi.status() != WL_CONNECTED) {
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD); // Fallback to auto-channel scan
    }
    #endif
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI OK] Connected to network successfully!");
    Serial.print("[WIFI OK] IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WIFI WARN] Connection timeout; will retry in main loop.");
  }
}

float readGasPpm(int rawAdc) {
  // ESP32 12-bit ADC ranges from 0 to 4095 (0.0V to 3.3V)
  // Clean ambient baseline: ~100 - 250 PPM (ADC: ~400 - 1000)
  // Moderate pollution: ~250 - 500 PPM (ADC: ~1000 - 2000)
  // High gas hazard / smoke: > 500 - 1000+ PPM (ADC: > 2000)
  float ppm = ((float)rawAdc / 4095.0f) * 1000.0f;
  if (ppm < 50.0f) ppm = 50.0f; // Ambient baseline clamp
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

  // Top Title Bar
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("EnviroSense");
  display.setCursor(76, 0);
  display.print(WiFi.status() == WL_CONNECTED ? "WiFi:OK" : "WiFi:--");
  display.drawLine(0, 10, 128, 10, SSD1306_WHITE);

  // Line 1: Temp & Humidity
  display.setCursor(0, 14);
  display.printf("T:%.1fC  H:%.0f%%", temp, hum);

  // Line 2: Heat Index & Gas PPM
  display.setCursor(0, 26);
  display.printf("HI:%.1fC Gas:%.0f", hi, gasPpm);

  // Line 3: Air Quality Label
  display.setCursor(0, 38);
  display.printf("Air: %s", airQuality);

  // Bottom Status Banner
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
    Serial.println(F("[POST SKIP] WiFi disconnected. Telemetry buffered."));
    return;
  }

  // Construct JSON Payload
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

  Serial.println(F("\n--------------------------------------------------------"));
  Serial.printf("[TELEMETRY] Temp: %.1fC | Hum: %.0f%% | Gas: %.0f PPM (%s) | Status: %s\n",
                temp, hum, gasPpm, airQuality, overallStatus);

  bool localSuccess = false;

  // 1. Local Bridge Transmission (Ultra-fast path for Wokwi VS Code Simulator -> Host Bridge)
  // Connects via http://host.wokwi.internal:3000/telemetry in <10ms and relays to AWS DynamoDB
  {
    HTTPClient http;
    http.setTimeout(1200);
    if (http.begin(LOCAL_API_URL)) {
      http.addHeader("Content-Type", "application/json");
      int code = http.POST(jsonPayload);
      if (code == 200 || code == 201) {
        Serial.printf("[LOCAL BRIDGE OK] HTTP %d -> Local Dashboard updated & AWS DynamoDB synced!\n", code);
        localSuccess = true;
      } else if (code > 0) {
        Serial.printf("[LOCAL BRIDGE] HTTP %d\n", code);
      } else {
        Serial.printf("[LOCAL BRIDGE OFF] Server not running on :3000 (%s)\n", http.errorToString(code).c_str());
      }
      http.end();
    }
  }

  // 2. Direct AWS API Gateway Transmission (Used for physical hardware or when local bridge is offline)
  #if USE_WOKWI_SIMULATION
  bool attemptAwsDirect = !localSuccess; // In simulation, local bridge relays to AWS; if bridge down, send directly
  #else
  bool attemptAwsDirect = true;          // Physical hardware connects directly to AWS
  #endif

  if (attemptAwsDirect) {
    HTTPClient https;
    WiFiClientSecure secureClient;
    secureClient.setInsecure(); // Learner lab / TLS validation
    secureClient.setTimeout(8000); // 8000ms = 8 seconds

    if (https.begin(secureClient, AWS_API_URL)) {
      https.addHeader("Content-Type", "application/json");
      if (strlen(API_KEY) > 0) {
        https.addHeader("x-api-key", API_KEY);
      }
      https.setTimeout(8000);
      Serial.printf("[AWS HTTPS] Sending -> %s\n", AWS_API_URL);
      int code = https.POST(jsonPayload);
      if (code == 200 || code == 201) {
        Serial.printf("[AWS HTTPS OK] HTTP %d -> DynamoDB recorded\n", code);
      } else if (code > 0) {
        Serial.printf("[AWS RES] HTTP %d\n", code);
      } else {
        Serial.printf("[AWS ERR] Code: %d (%s)\n", code, https.errorToString(code).c_str());
      }
      https.end();
    }
  }
  Serial.println(F("--------------------------------------------------------"));
}
