# base_station_server.py
import socket, json, csv, datetime, os

HOST = "0.0.0.0"
PORT = 5000          # local port playit forwards to
LOG_FILE = "sensor_log.csv"

THRESHOLDS = {
    "temp":  (18, 35),
    "hum":   (40, 70),
    "conc":  (0,  2.5),
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
    print(f"[Server] UDP listening on port {PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        while True:
            data, addr = s.recvfrom(1024)
            try:
                packet = json.loads(data.decode())
                print(f"\n[Data from {addr}] {packet}")
                alerts = check_alerts(packet)
                for a in alerts: print(a)
                log_to_csv(packet)
            except json.JSONDecodeError:
                print(f"[Error] Bad packet: {data}")

if __name__ == "__main__":
    main()
