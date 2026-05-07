#include <Wire.h>
#include <U8g2lib.h>
#include <DHT.h>
#include <WiFi.h>

#define OLED_RESET -1
#define DHTPIN     4
#define DHTTYPE    DHT22

// Wokwi's simulated WiFi credentials
const char* ssid     = "Wokwi-GUEST";
const char* password = "";

// Your laptop's IP + port
const char* serverIP   = "192.168.192.51";  // e.g. "192.168.1.10"
const int   serverPort = 5000;

U8G2_SH1107_128X128_1_HW_I2C display(U8G2_R0, OLED_RESET);
DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;

const int airpin  = 15;
const int conc    = 34;
const int buzzpin = 2;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  display.begin();
  display.setFont(u8g2_font_6x10_tf);
  dht.begin();
  pinMode(airpin,  INPUT);
  pinMode(buzzpin, OUTPUT);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  display.firstPage();
  do {
    display.setCursor(0, 10);
    display.print("Connecting WiFi...");
  } while (display.nextPage());

  while (WiFi.status() != WL_CONNECTED) delay(500);

  display.firstPage();
  do {
    display.setCursor(0, 10);
    display.print("WiFi OK");
    display.setCursor(0, 20);
    display.print(WiFi.localIP());
  } while (display.nextPage());

  delay(1000);
}

void loop() {
  float humidity      = dht.readHumidity();
  float temperature   = dht.readTemperature();
  int   airquality    = digitalRead(airpin);
  float concentration = (3.3f / 4095.0f) * analogRead(conc);
  bool  buzzerNeeded  = false;

  // --- Send to server ---
  if (!client.connected()) {
    client.connect(serverIP, serverPort);
  }
  if (client.connected()) {
    String json = "{";
    json += "\"temp\":"  + String(temperature, 2) + ",";
    json += "\"hum\":"   + String(humidity, 2)    + ",";
    json += "\"conc\":"  + String(concentration, 3) + ",";
    json += "\"air\":"   + String(airquality);
    json += "}\n";
    client.print(json);
  }

  // --- Display ---
  display.firstPage();
  do {
    display.setCursor(0, 10);
    display.print("Temp: "); display.print(temperature, 1); display.print("C");

    if (temperature < 18)      { buzzerNeeded = true; display.setCursor(0,20); display.print("Temp LOW");  }
    else if (temperature > 35) { buzzerNeeded = true; display.setCursor(0,20); display.print("Temp HIGH"); }

    display.setCursor(0, 40);
    display.print("Hum: "); display.print(humidity, 1); display.print("%");

    if (humidity < 40)      { buzzerNeeded = true; display.setCursor(0,50); display.print("Humid LOW");  }
    else if (humidity > 70) { buzzerNeeded = true; display.setCursor(0,50); display.print("Humid HIGH"); }

    display.setCursor(0, 70);
    display.print("Conc: "); display.print(concentration, 3); display.print("V");

    if (airquality == LOW) { buzzerNeeded = true; display.setCursor(0,80); display.print("Air BAD"); }

    display.setCursor(0, 100);
    display.print(client.connected() ? "Server: OK" : "Server: --");

  } while (display.nextPage());

  digitalWrite(buzzpin, buzzerNeeded ? HIGH : LOW);
  delay(3000);
  digitalWrite(buzzpin, LOW);
}
