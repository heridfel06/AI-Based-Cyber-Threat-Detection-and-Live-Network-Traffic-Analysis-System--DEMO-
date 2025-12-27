import pandas as pd
import os

# -----------------------------
# Path configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

TRAIN_FILE = os.path.join(DATA_DIR, "KDDTrain+.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "training_dataset.csv")

# -----------------------------
# NSL-KDD column names
# -----------------------------
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files",
    "num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
]

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(TRAIN_FILE, names=columns)

# -----------------------------
# Feature selection (correct)
# -----------------------------
processed = pd.DataFrame()

processed["packet_count"] = df["count"]
processed["unique_dst_ports"] = df["srv_count"]
processed["avg_packet_size"] = df["src_bytes"] + df["dst_bytes"]
processed["tcp_flag"] = (df["protocol_type"] == "tcp").astype(int)
processed["udp_flag"] = (df["protocol_type"] == "udp").astype(int)
processed["flow_duration"] = df["duration"]

# -----------------------------
# Label encoding
# -----------------------------
processed["label"] = (df["label"] != "normal").astype(int)

# -----------------------------
# Save dataset
# -----------------------------
processed.to_csv(OUTPUT_FILE, index=False)

print("TASK 4 completed successfully (corrected).")
print(f"Saved to: {OUTPUT_FILE}")
print(processed.head())
