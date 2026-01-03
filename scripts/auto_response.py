import os
import time
from collections import defaultdict
from datetime import datetime

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALERT_DIR = os.path.join(BASE_DIR, "alerts")

ALERT_FILE = os.path.join(ALERT_DIR, "alerts.log")
RESPONSE_FILE = os.path.join(ALERT_DIR, "response.log")

os.makedirs(ALERT_DIR, exist_ok=True)

print("Automated Response Engine Started (Simulation Mode)")
print("-" * 55)

# -----------------------------
# State tracking
# -----------------------------
alert_counts = defaultdict(int)
blocked_ips = set()
last_processed_line = 0

# -----------------------------
# Log response safely
# -----------------------------
def log_response(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(RESPONSE_FILE, "a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())

# -----------------------------
# Main loop
# -----------------------------
while True:
    if not os.path.exists(ALERT_FILE):
        time.sleep(2)
        continue

    with open(ALERT_FILE, "r") as f:
        lines = f.readlines()

    new_lines = lines[last_processed_line:]

    for line in new_lines:
        # Extract source IP
        if "SRC=" in line:
            src_ip = line.split("SRC=")[1].split("|")[0].strip()
            alert_counts[src_ip] += 1

            if alert_counts[src_ip] >= 3 and src_ip not in blocked_ips:
                blocked_ips.add(src_ip)
                log_response(
                    f"[RESPONSE] SRC={src_ip} | ACTION=BLOCK (SIMULATED) | "
                    f"ALERT_COUNT={alert_counts[src_ip]}"
                )

    last_processed_line = len(lines)
    time.sleep(2)
