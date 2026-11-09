# EnviroSense — Microcontroller Wiring Schematic & Hardware Pinout

Course: **Cloud Computing (25CAI102PC205)** · Product #23 · SR University

---

## 1. Components List
| Component | Description | Quantity |
| :--- | :--- | :--- |
| **ESP32 NodeMCU DevKit V1** | 30/38-pin Wi-Fi + BLE Microcontroller | 1 |
| **DHT11 (or DHT22)** | Digital Temperature & Humidity Sensor | 1 |
| **SSD1306 0.96" OLED** | 128x64 Monochrome I2C Display | 1 |
| **Pull-up Resistor** | 4.7kΩ or 10kΩ (optional if DHT breakout module has onboard resistor) | 1 |
| **Jumper Wires & Breadboard** | Female-to-Male and Male-to-Male | 8 |
| **Micro-USB Cable** | Data cable for power & flashing firmware | 1 |

---

## 2. Pin Connection Table

### A. DHT11 / DHT22 Sensor Connection
| DHT Pin | Description | ESP32 Connection | Notes |
| :--- | :--- | :--- | :--- |
| **VCC / +** | Power (3.3V - 5V) | `3V3` (Pin 1 or 3.3V) | Connect to regulated 3.3V |
| **DATA / OUT** | Digital Signal | `GPIO 4` (D4) | Signal line |
| **GND / -** | Ground | `GND` | Common ground |

### B. SSD1306 OLED (I2C) Connection
| OLED Pin | Description | ESP32 Connection | Notes |
| :--- | :--- | :--- | :--- |
| **VCC** | Power Supply | `3V3` | 3.3V rail |
| **GND** | Ground | `GND` | Common ground |
| **SCL** | I2C Clock | `GPIO 22` | ESP32 hardware I2C clock |
| **SDA** | I2C Data | `GPIO 21` | ESP32 hardware I2C data |

---

## 3. Circuit Wiring Schematic (ASCII)

```text
               +----------------------------------+
               |        ESP32 DEVKIT V1           |
               |                                  |
               | [3V3]----------------+           |
               |                      |           |
               | [GND]-------------+  |           |
               |                   |  |           |
               | [GPIO 4]-----+    |  |           |
               |              |    |  |           |
               | [GPIO 21]--+ |    |  |           |
               | [GPIO 22]-+| |    |  |           |
               +-----------||-|----+--+-----------+
                           || |    |  |
             +-------------+| |    |  |
             | +------------+ |    |  |
             | |              |    |  |
             | |              |    |  +--------+--------+
             | |              |    +-----+     |        |
             | |              |          |     |        |
             | |           +--+---+      |     |        |
             | |           | DATA |      |     |        |
             | |           | VCC  |<-----+     |        |
             | |           | GND  |<-----------+        |
             | |           +------+                     |
             | |           DHT11 SENSOR                 |
             | |                                        |
             | |           +---------------+            |
             | +---------->| SDA           |            |
             +------------>| SCL           |            |
                           | GND           |<-----------+
                           | VCC           |<-----------+
                           +---------------+
                           SSD1306 0.96" OLED
```

---

## 4. Flashing Instructions (Arduino IDE)
1. Open **Arduino IDE**.
2. Go to **File > Preferences**, and add the ESP32 board manager URL:
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. Go to **Tools > Board > Boards Manager**, search for `esp32` by Espressif Systems, and install.
4. Install libraries via **Sketch > Include Library > Manage Libraries**:
   - `DHT sensor library` by Adafruit
   - `Adafruit SSD1306` by Adafruit
   - `Adafruit GFX Library` by Adafruit
   - `ArduinoJson` by Benoit Blanchon
5. Open `firmware/esp32_dht11_oled.ino`.
6. Update `WIFI_SSID`, `WIFI_PASSWORD`, and `API_URL` with your network and AWS API Gateway endpoint.
7. Select Board: `DOIT ESP32 DEVKIT V1` and your COM port.
8. Click **Upload**. Open **Serial Monitor** (115200 baud) to watch real-time sensor readings and HTTP publication.
