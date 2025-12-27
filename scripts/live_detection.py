import pandas as pd
import joblib
import os
import time
import warnings

# Suppress sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

FEATURE_FILE = os.path.join(DATA_DIR, "live_features.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "attack_model.pkl")

FEATURE_COLUMNS = [
    "packet_count",
    "unique_dst_ports",
    "avg_packet_size",
    "tcp_flag",
    "udp_flag",
    "flow_duration"
]

model = joblib.load(MODEL_FILE)

print("ML Detection Engine Started")
print("-" * 50)

last_index = -1

while True:
    if not os.path.exists(FEATURE_FILE):
        time.sleep(2)
        continue

    df = pd.read_csv(FEATURE_FILE)
    new_rows = df.iloc[last_index + 1:]

    for idx, row in new_rows.iterrows():
        X = pd.DataFrame([row[FEATURE_COLUMNS]])

        prediction = model.predict(X)[0]
        label = "ATTACK" if prediction == 1 else "NORMAL"

        print(f"[ML] SRC={row['src_ip']} | RESULT={label}")

        last_index = idx

    time.sleep(2)
