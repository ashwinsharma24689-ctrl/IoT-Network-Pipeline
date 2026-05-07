# base_station_server.py
import socket, json, csv, datetime, os

HOST = "0.0.0.0"
PORT = 5000
LOG_FILE = "sensor_log.csv"

THRESHOLDS = {
    "temp":  (18, 35),
    "hum":   (40, 70),
    "conc":  (0,  2.5),   # volts — adjust to your sensor
}

def check_alerts(data):
    alerts = []
    for key, (low, high) in THRESHOLDS.items():
        val = data.get(key)
        if val is None: continue
        if val < low:   alerts.append(f"⚠️  {key} LOW:  {val}")
        if val > high:  alerts.append(f"🚨 {key} HIGH: {val}")
    if data.get("air") == 0:
        alerts.append("🚨 Air quality BAD")
    return alerts

def log_to_csv(data):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp","temp","hum","conc","air"])
        if not file_exists:
            writer.writeheader()
        data["timestamp"] = datetime.datetime.now().isoformat()
        writer.writerow(data)

def main():
    print(f"[Server] Listening on port {PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print(f"[Server] ESP32 connected from {addr}")
        with conn:
            buffer = ""
            while True:
                chunk = conn.recv(1024).decode()
                if not chunk:
                    print("[Server] ESP32 disconnected")
                    break
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    try:
                        data = json.loads(line.strip())
                        print(f"\n[Data] {data}")
                        alerts = check_alerts(data)
                        for a in alerts: print(a)
                        log_to_csv(data)
                    except json.JSONDecodeError:
                        pass

if __name__ == "__main__":
    main()
