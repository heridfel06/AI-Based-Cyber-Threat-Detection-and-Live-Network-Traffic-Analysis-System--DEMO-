from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
import pandas as pd
from datetime import datetime
import os

# Resolve base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_CSV = os.path.join(DATA_DIR, "live_packets.csv")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

packet_data = []

def packet_handler(packet):
    if IP in packet:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        length = len(packet)

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

        packet_data.append([
            timestamp,
            src_ip,
            dst_ip,
            protocol,
            src_port,
            dst_port,
            length
        ])

        print(f"[{timestamp}] {src_ip} -> {dst_ip} | {protocol} | {length} bytes")

def save_to_csv():
    if not packet_data:
        print("No packets captured. CSV not created.")
        return

    df = pd.DataFrame(packet_data, columns=[
        "timestamp",
        "src_ip",
        "dst_ip",
        "protocol",
        "src_port",
        "dst_port",
        "packet_length"
    ])

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nCSV saved successfully at:\n{OUTPUT_CSV}")

try:
    print("Starting live packet capture... Press CTRL+C to stop.\n")
    sniff(prn=packet_handler, store=False)
except KeyboardInterrupt:
    print("\nStopping capture...")
    save_to_csv()
