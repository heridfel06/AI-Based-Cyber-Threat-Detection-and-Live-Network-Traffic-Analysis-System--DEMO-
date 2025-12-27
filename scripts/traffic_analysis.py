import pandas as pd
import os
import matplotlib.pyplot as plt

# -----------------------------
# Path configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")

INPUT_CSV = os.path.join(DATA_DIR, "live_packets.csv")

os.makedirs(ANALYSIS_DIR, exist_ok=True)

# -----------------------------
# Load live packet data
# -----------------------------
df = pd.read_csv(INPUT_CSV)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -----------------------------
# 1. Traffic Volume vs Time
# -----------------------------
traffic_time = df.set_index("timestamp").resample("5s").size()

if len(traffic_time) > 1:
    plt.figure()
    traffic_time.plot()
    plt.xlabel("Time")
    plt.ylabel("Packet Count")
    plt.title("Traffic Volume vs Time")
    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSIS_DIR, "traffic_volume_time.png"))
    plt.close()
else:
    print("Not enough time variance for traffic volume plot.")

# -----------------------------
# 2. Protocol Distribution
# -----------------------------
protocol_counts = df["protocol"].value_counts()

plt.figure()
protocol_counts.plot(kind="bar")
plt.xlabel("Protocol")
plt.ylabel("Packet Count")
plt.title("Protocol Distribution")
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, "protocol_distribution.png"))
plt.close()

# -----------------------------
# 3. Top Source IPs
# -----------------------------
top_sources = df["src_ip"].value_counts().head(10)

plt.figure()
top_sources.plot(kind="bar")
plt.xlabel("Source IP")
plt.ylabel("Packet Count")
plt.title("Top Source IPs by Packet Count")
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DIR, "top_source_ips.png"))
plt.close()

print("TASK 7 completed successfully.")
print(f"Plots saved in: {ANALYSIS_DIR}")
