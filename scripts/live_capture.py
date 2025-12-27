from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
import pandas as pd
from datetime import datetime
import os
import signal
import sys

# -------------------------------
# Path configuration (Windows-safe)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_CSV = os.path.join(DATA_DIR, "live_packets.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------
# Runtime configuration
# -------------------------------
SAVE_INTERVAL = 25   # save after every 25 packets
packet_buffer = []

# -------------------------------
# CSV persistence logic
# -------------------------------
def save_packets():
    if not packet_buffer:
        return

    df = pd.DataFrame(packet_buffer, columns=[
        "timestamp",
        "src_ip",
        "dst_ip",
        "protocol",
        "src_port",
        "dst_port",
        "packet_length"
    ])

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"[INFO] Packets saved to CSV: {OUTPUT_CSV}")

# -------------------------------
# Packet processing
# -------------------------------
def packet_handler(packet):
    if IP not in packet:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    packet_length = len(packet)

    src_port = None
    dst_port = None

    if TCP in packet:
        protocol = "TCP"
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif UDP in packet:
        protocol = "UDP"
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    else:
        protocol = "OTHER"

    packet_buffer.append([
        timestamp,
        src_ip,
        dst_ip,
        protocol,
        src_port,
        dst_port,
        packet_length
    ])

    print(f"[{timestamp}] {src_ip} -> {dst_ip} | {protocol} | {packet_length} bytes")

    if len(packet_buffer) % SAVE_INTERVAL == 0:
        save_packets()

# -------------------------------
# Graceful shutdown handling
# -------------------------------
def shutdown_handler(sig, frame):
    print("\n[INFO] Capture stopping. Saving remaining packets...")
    save_packets()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# -------------------------------
# Start capture
# -------------------------------
print("Starting live packet capture (Windows-safe mode)")
print("CSV will be saved automatically during capture\n")

sniff(prn=packet_handler, store=False)
