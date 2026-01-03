import pandas as pd
import joblib
import os
import time

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

FEATURE_FILE = os.path.join(DATA_DIR, "live_features.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "anomaly_model.pkl")

print("Anomaly Detection Engine Started")
print("-" * 50)

# -----------------------------
# Load model
# -----------------------------
model = joblib.load(MODEL_FILE)

last_index = -1

while True:
    if not os.path.exists(FEATURE_FILE):
        time.sleep(2)
        continue

    df = pd.read_csv(FEATURE_FILE)
    new_rows = df.iloc[last_index + 1:]

    for idx, row in new_rows.iterrows():

        # ---- FIX: derive flags ----
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

        pred = model.predict(X)[0]           # -1 = anomaly, 1 = normal
        score = model.decision_function(X)[0]

        status = "ANOMALOUS" if pred == -1 else "NORMAL"

        print(
            f"[ANOMALY] SRC={row['src_ip']} | "
            f"STATUS={status} | SCORE={score:.3f}"
        )

        last_index = idx

    time.sleep(2)
