# 🌿 Environment Quality Detection System

A networked environmental monitoring system built on the ESP32 microcontroller. Reads temperature, humidity, and air quality data from DHT22 and MQ2 sensors, displays live readings on an SH1107 OLED screen, and streams data over WiFi via TCP to a Python base station server that logs readings to CSV and triggers alerts for out-of-range values.

---

## 📸 Demo

> Simulated on [Wokwi](https://wokwi.com) — ESP32 streams live sensor data to a Python server over TCP via ngrok tunnel.

---

## 🧰 Hardware Components

| Component | Description |
|-----------|-------------|
| ESP32 DevKit C V4 | Main microcontroller |
| DHT22 | Temperature & humidity sensor |
| MQ2 Gas Sensor | Air quality / gas concentration sensor |
| SH1107 OLED (128x128) | Display for live readings |
| Buzzer | Audio alert for out-of-range values |

---

## 📐 Wiring

### DHT22
| DHT22 Pin | ESP32 Pin |
|-----------|-----------|
| VCC | 5V |
| GND | GND |
| SDA | GPIO4 |

### MQ2 Gas Sensor
| MQ2 Pin | ESP32 Pin |
|---------|-----------|
| VCC | 5V |
| GND | GND |
| AOUT | GPIO34 |
| DOUT | GPIO15 |

### SH1107 OLED
| OLED Pin | ESP32 Pin |
|----------|-----------|
| VCC | 5V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

### Buzzer
| Buzzer Pin | ESP32 Pin |
|------------|-----------|
| + | GPIO2 |
| - | GND |

> ⚠️ **Important:** ESP32 GPIO pins are **3.3V tolerant only**. Use a voltage divider on MQ2's AOUT and DOUT pins since the sensor runs on 5V.

---

## 🗂️ Project Structure

```
environment-quality-detection/
├── sketch.ino               # ESP32 Arduino sketch
├── python base station.py   # Python TCP server
├── diagram.json             # Wokwi circuit diagram
├── libraries.txt            # Wokwi library dependencies
└── README.md
```

---

## 📦 Dependencies

### Arduino Libraries (Wokwi / Arduino IDE)
- `Wire`
- `U8g2`
- `DHT sensor library`
- `WiFi` (built-in with ESP32)

### Python
- Python 3.x
- Standard library only (`socket`, `json`, `csv`, `datetime`, `os`)

---

## 🚀 Setup & Usage

### 1. Wokwi Simulation

1. Open [Wokwi](https://wokwi.com) and create a new **ESP32 Arduino** project
2. Paste `sketch.ino` into the editor
3. Replace `diagram.json` with the one from this repo
4. Add libraries via the **Library Manager**:
   - DHT sensor library
   - U8g2
   - Wire
5. Update the server IP and port in `sketch.ino`:
   ```cpp
   const char* serverIP   = "YOUR_NGROK_HOST";
   const int   serverPort = YOUR_NGROK_PORT;
   ```

### 2. Python Base Station

```bash
python "python base station.py"
```

The server will start listening on port `5000`:
```
[Server] Listening on port 5000...
```

### 3. Expose Local Server via ngrok

Since Wokwi runs in the cloud, use [ngrok](https://ngrok.com) to tunnel your local server:

```bash
ngrok tcp 5000
```

Copy the forwarding address (e.g. `0.tcp.ngrok.io:12345`) and update `sketch.ino` with the host and port.

### 4. Run

1. Start the Python server first
2. Start ngrok
3. Update `sketch.ino` with the ngrok address
4. Press ▶ Play in Wokwi
5. Watch live data stream into your terminal

---

## 📊 Data Logging

Sensor readings are automatically saved to `sensor_log.csv`:

```
timestamp,temp,hum,conc,air
2026-05-07T04:30:00,24.0,60.0,0.123,1
2026-05-07T04:30:03,24.1,59.8,0.120,1
...
```

---

## 🚨 Alert Thresholds

| Parameter | Low | High |
|-----------|-----|------|
| Temperature | < 18°C | > 35°C |
| Humidity | < 40% | > 70% |
| Air Quality (DOUT) | — | `LOW` = Bad |

When a threshold is breached:
- 🔔 Buzzer activates on the ESP32
- ⚠️ Alert printed in the Python server terminal
- 📟 Warning message shown on OLED

---

## 🛠️ Built With

- [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- [U8g2 Library](https://github.com/olikraus/u8g2)
- [DHT Sensor Library](https://github.com/adafruit/DHT-sensor-library)
- [Wokwi Simulator](https://wokwi.com)
- [ngrok](https://ngrok.com)

---

## 👤 Author

**ash_0651**  
[GitHub](https://github.com/ashwinsharma24689)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
