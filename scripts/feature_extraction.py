import pandas as pd
import os

# -------------------------------
# Path configuration
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_CSV = os.path.join(DATA_DIR, "live_packets.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "live_features.csv")

WINDOW_SIZE = 5  # seconds

# -------------------------------
# Validation
# -------------------------------
if not os.path.exists(INPUT_CSV):
    raise FileNotFoundError(f"Input file not found: {INPUT_CSV}")

# -------------------------------
# Load packet data
# -------------------------------
df = pd.read_csv(INPUT_CSV)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# -------------------------------
# Create time windows
# -------------------------------
df["time_window"] = df["timestamp"].dt.floor(f"{WINDOW_SIZE}s")

# -------------------------------
# Feature aggregation
# -------------------------------
features = []

for (src_ip, window), group in df.groupby(["src_ip", "time_window"]):
    packet_count = len(group)
    unique_dst_ports = group["dst_port"].nunique()
    avg_packet_size = group["packet_length"].mean()
    tcp_count = (group["protocol"] == "TCP").sum()
    udp_count = (group["protocol"] == "UDP").sum()
    flow_duration = (
        group["timestamp"].max() - group["timestamp"].min()
    ).total_seconds()

    features.append([
        src_ip,
        window,
        packet_count,
        unique_dst_ports,
        avg_packet_size,
        tcp_count,
        udp_count,
        flow_duration
    ])

# -------------------------------
# Create feature DataFrame
# -------------------------------
feature_df = pd.DataFrame(features, columns=[
    "src_ip",
    "window_start",
    "packet_count",
    "unique_dst_ports",
    "avg_packet_size",
    "tcp_count",
    "udp_count",
    "flow_duration"
])

# -------------------------------
# Save features
# -------------------------------
feature_df.to_csv(OUTPUT_CSV, index=False)


print(f"Feature file saved at:\n{OUTPUT_CSV}")
print("\nSample output:")
print(feature_df.head())
