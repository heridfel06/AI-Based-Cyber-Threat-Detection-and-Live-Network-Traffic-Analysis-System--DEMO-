import pandas as pd
import joblib
import os
import time
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# =============================
# PATHS
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
ALERT_DIR = os.path.join(BASE_DIR, "alerts")

FEATURE_FILE = os.path.join(DATA_DIR, "live_features.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "attack_model.pkl")
ALERT_FILE = os.path.join(ALERT_DIR, "alerts.log")

os.makedirs(ALERT_DIR, exist_ok=True)

# =============================
# CONFIG
# =============================
PORT_SCAN_THRESHOLD = 20
TIME_WINDOW_SECONDS = 5

FEATURE_COLUMNS = [
    "packet_count",
    "unique_dst_ports",
    "avg_packet_size",
    "tcp_flag",
    "udp_flag",
    "flow_duration"
]

# =============================
# STARTUP INFO
# =============================
print("\n=========== ALERT ENGINE (DECISION MODE) ===========")
print("Feature file :", FEATURE_FILE)
print("Model file   :", MODEL_FILE)
print("Alert file   :", ALERT_FILE)
print("===================================================\n")

# =============================
# LOAD MODEL
# =============================
model = joblib.load(MODEL_FILE)

last_index = -1

# =============================
# LOGGING
# =============================
def log_alert(text):
    with open(ALERT_FILE, "a") as f:
        f.write(text + "\n")
        f.flush()
        os.fsync(f.fileno())

# =============================
# MAIN LOOP
# =============================
while True:
    if not os.path.exists(FEATURE_FILE):
        time.sleep(2)
        continue

    df = pd.read_csv(FEATURE_FILE)
    new_rows = df.iloc[last_index + 1:]

    for idx, row in new_rows.iterrows():

        # Derive protocol flags safely
        tcp_flag = 1 if row["tcp_count"] > 0 else 0
        udp_flag = 1 if row["udp_count"] > 0 else 0

        X = pd.DataFrame([{
            "packet_count": row["packet_count"],
            "unique_dst_ports": row["unique_dst_ports"],
            "avg_packet_size": row["avg_packet_size"],
            "tcp_flag": tcp_flag,
            "udp_flag": udp_flag,
            "flow_duration": row["flow_duration"]
        }])

        # ML prediction + confidence
        ml_prediction = model.predict(X)[0]
        ml_confidence = max(model.predict_proba(X)[0])

        # Rule-based suspicion
        rule_suspicious = row["unique_dst_ports"] > PORT_SCAN_THRESHOLD

        # -----------------------------
        # SECURITY DECISION
        # -----------------------------
        if rule_suspicious and ml_prediction == 1:
            severity = "HIGH"
            alert_type = "Possible Port Scan"
        elif ml_prediction == 1:
            severity = "MEDIUM"
            alert_type = "Suspicious Traffic"
        else:
            severity = "LOW"
            alert_type = "Normal Activity"

        # Only log meaningful security decisions
        if severity != "LOW":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            alert_text = (
                f"[{timestamp}] ALERT: {alert_type}\n"
                f"Source IP: {row['src_ip']}\n"
                f"Decision Basis:\n"
                f"- Unique destination ports: {row['unique_dst_ports']} "
                f"(threshold = {PORT_SCAN_THRESHOLD})\n"
                f"- Time window: {TIME_WINDOW_SECONDS} seconds\n"
                f"- ML confidence score: {ml_confidence:.2f}\n"
                f"Final decision: {severity} severity\n"
                f"{'-'*50}"
            )

            print(alert_text)
            log_alert(alert_text)

        last_index = idx

    time.sleep(2)
