# EnviroSense — Microcontroller Wiring Schematic & Hardware Pinout

Course: **Cloud Computing (25CAI102PC205)** · Product #23 · SR University  
Hardware Node: **ESP32 DevKit V1 + DHT22 (Temp & Humidity) + MQ-135 (Gas & Air Quality) + SSD1306 OLED**

---

## 1. Components List
| Component | Description | Quantity | Operational Specs |
| :--- | :--- | :--- | :--- |
| **ESP32 NodeMCU DevKit V1** | 30/38-pin Wi-Fi + BLE Microcontroller | 1 | 240 MHz Dual Core, 3.3V Logic |
| **DHT22 (AM2302)** | Precision Digital Temp & Humidity Sensor | 1 | -40 to 80°C (±0.5°C), 0-100% RH (±2%) |
| **MQ-135 Gas Sensor** | Hazardous Gas & Air Quality Electrochemical Sensor | 1 | Detects CO2, NOx, Smoke, NH3, Benzene (0-1000 PPM) |
| **SSD1306 0.96" OLED** | 128x64 Monochrome I2C Graphical Display | 1 | I2C address `0x3C`, 3.3V supply |
| **Pull-up Resistor** | 4.7kΩ or 10kΩ (included on DHT breakout boards) | 1 | Pull-up on DHT22 DATA line |
| **Breadboard & Jumpers** | DuPont Jumper Wires (F-M, M-M) | 12 | Standard 0.1" pitch breadboard |

---

## 2. Complete Pin Connection Table

### A. DHT22 Temperature & Humidity Sensor
| DHT22 Pin | Description | ESP32 Pin Connection | Wire Color | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **VCC (+)** | Power Supply | `3V3` | Red | 3.3V Power rail |
| **DATA (OUT)** | Digital 1-Wire Data | `GPIO 4` (D4) | Gold / Yellow | Digital input with internal pull-up |
| **NC** | Not Connected | None | — | Leave floating (4-pin DHT22 models) |
| **GND (-)** | Ground | `GND` | Black | Common circuit ground |

### B. MQ-135 Air Quality & Gas Detection Sensor
| MQ-135 Pin | Description | ESP32 Pin Connection | Wire Color | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **VCC** | Power Supply | `5V` (or `3V3`) | Red | 5V / VIN rail recommended for heater coil |
| **GND** | Ground | `GND` | Black | Common circuit ground |
| **AOUT** | Analog Gas Output | `GPIO 34` (ADC1_CH6) | Blue | **Must use ADC1** (ADC2 conflicts with ESP32 Wi-Fi) |
| **DOUT** | Digital Threshold Trip | `GPIO 35` (ADC1_CH7) | Cyan | Optional digital threshold comparator trip |

### C. SSD1306 0.96" I2C OLED Display
| OLED Pin | Description | ESP32 Pin Connection | Wire Color | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **VCC** | Display Power | `3V3` | Red | 3.3V supply rail |
| **GND** | Ground | `GND` | Black | Common ground |
| **SDA** | I2C Data Line | `GPIO 21` (D21) | Green | Hardware I2C SDA bus |
| **SCL** | I2C Clock Line | `GPIO 22` (D22) | Orange | Hardware I2C SCL bus |

---

## 3. Circuit Wiring Schematic (ASCII Diagram)

```text
               +-------------------------------------------+
               |              ESP32 DEVKIT V1              |
               |                                           |
               | [3V3]-------------------+---+             |
               | [5V / VIN]-----------+  |   |             |
               | [GND]--------------+-|--|---|----+        |
               |                    | |  |   |    |        |
               | [GPIO 4]-------+   | |  |   |    |        |
               | [GPIO 34]----+ |   | |  |   |    |        |
               | [GPIO 35]--+ | |   | |  |   |    |        |
               |            | | |   | |  |   |    |        |
               | [GPIO 21]-+|| | |  | |  |   |    |        |
               | [GPIO 22]+||| | |  | |  |   |    |        |
               +----------||||-|-|--|-|--|---|----+--------+
                          |||| | |  | |  |   |    |
           +--------------+||| | |  | |  |   |    |
           | +-------------+|| | |  | |  |   |    |
           | |              || | |  | |  |   |    |
           | | +------------+| | |  | |  |   |    |
           | | | +-----------+ | |  | |  |   |    |
           | | | |             | |  | |  |   |    |
           | | | |   +---------+-+  | |  |   |    |
           | | | |   |              | |  |   |    |
           | | | |   |     +--------+-+--+   |    |
           | | | |   |     |                 |    |
           | | | |   |     |  DHT22 SENSOR   |    |
           | | | |   |     |  +------------+ |    |
           | | | |   |     |  | VCC        |<+    |
           | | | |   |     |  | DATA       |<-----+ [GPIO 4]
           | | | |   |     +->| GND        |
           | | | |   |        +------------+
           | | | |   |
           | | | |   |        MQ-135 SENSOR
           | | | |   |        +------------+
           | | | |   |        | VCC        |<-----+ [5V]
           | | | |   +------->| GND        |
           | | | +----------->| AOUT       |------+ [GPIO 34 (ADC1)]
           | | +------------->| DOUT       |------+ [GPIO 35 (Threshold)]
           | |                +------------+
           | |
           | |                SSD1306 OLED
           | |                +------------+
           | +--------------->| SDA (21)   |
           +----------------->| SCL (22)   |
                              | VCC (3V3)  |<-----+ [3V3]
                              | GND        |<-----+ [GND]
                              +------------+
```

---

## 4. Virtual Simulation in VS Code via Wokwi

EnviroSense is configured for zero-hardware virtual simulation using the **Wokwi for VS Code** extension:

### Files:
- **`diagram.json`**: Declares the virtual ESP32 DevKit, DHT22 sensor, MQ-135 gas sensor, SSD1306 OLED screen, and wire routes.
- **`wokwi.toml`**: Points the Wokwi engine directly to the compiled `.pio/build/esp32dev/firmware.bin` and `.elf`.
- **`server.py`**: Local HTTP bridge running on your machine. Receives telemetry from the Wokwi ESP32 via `http://host.wokwi.internal:3000/telemetry` and serves the web dashboard at `http://localhost:3000`.

### Quick Start Instructions:
1. Open VS Code in the project folder.
2. Ensure **Wokwi for VS Code** extension is installed (`wokwi.wokwi-vscode`).
3. Start the local bridge server in your terminal:
   ```powershell
   python server.py 3000
   ```
4. Open `diagram.json` in VS Code.
5. Press **F1** (or `Ctrl+Shift+P`) and choose:
   ```text
   Wokwi: Start Simulator
   ```
6. The interactive virtual ESP32 appears in VS Code!
   - Click the **DHT22** sensor to drag temperature & humidity sliders.
   - Click the **MQ-135** gas sensor to slide the gas concentration level.
   - The virtual **SSD1306 OLED** updates immediately with live readings.
   - The ESP32 sends telemetry to the local bridge server via Wi-Fi (`Wokwi-GUEST`).
   - The browser dashboard at `http://localhost:3000` receives the live readings in real time!

---

## 5. Physical Hardware Flashing Instructions

### Using PlatformIO (VS Code):
1. Connect physical ESP32 to USB.
2. In `firmware/src/main.cpp`, change:
   ```cpp
   #define USE_WOKWI_SIMULATION 0
   ```
   and enter your Wi-Fi SSID, password, and deployed AWS API Gateway URL.
3. Click the PlatformIO **Upload** icon (`→`) in the VS Code bottom status bar, or run:
   ```powershell
   pio run --target upload
   ```

### Using Arduino IDE:
1. Open `firmware/esp32_dht22_mq135_oled.ino`.
2. Install libraries:
   - `DHT sensor library` by Adafruit
   - `Adafruit SSD1306` by Adafruit
   - `Adafruit GFX Library` by Adafruit
   - `ArduinoJson` by Benoit Blanchon
3. Update Wi-Fi and API Gateway parameters.
4. Select board **DOIT ESP32 DEVKIT V1**, select your COM port, and click **Upload**.
