import pandas as pd
import joblib
import os
import time
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# =============================
# PATH CONFIGURATION
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
# STARTUP INFO
# =============================
print("\n=========== ALERT ENGINE STARTED ===========")
print("FEATURE FILE:", FEATURE_FILE)
print("MODEL FILE  :", MODEL_FILE)
print("ALERT FILE  :", ALERT_FILE)
print("===========================================\n")

# =============================
# LOAD MODEL
# =============================
model = joblib.load(MODEL_FILE)

last_index = -1

# =============================
# SAFE LOG FUNCTION
# =============================
def log_alert(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(ALERT_FILE, "a") as f:
        f.write(line + "\n")
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

        # ---- FIX: derive flags from counts ----
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

        prediction = model.predict(X)[0]

        reasons = []

        if prediction == 1:
            reasons.append("ML_ATTACK")

        if row["unique_dst_ports"] > 20:
            reasons.append("PORT_SCAN")

        if reasons:
            log_alert(
                f"ALERT | SRC={row['src_ip']} | REASON={' + '.join(reasons)}"
            )

        last_index = idx

    time.sleep(2)
