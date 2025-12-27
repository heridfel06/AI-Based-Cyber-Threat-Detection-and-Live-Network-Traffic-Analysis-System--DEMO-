import subprocess
import sys
import os
import time

# -----------------------------
# Path configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    return subprocess.Popen(
        [sys.executable, script_path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

print("====================================")
print(" AI-Based Cyber Threat Detection Demo ")
print("====================================\n")

# 1. Live Packet Capture
print("[1/5] Starting live packet capture...")
run_script("live_capture.py")
time.sleep(5)

# 2. Feature Extraction
print("[2/5] Starting feature extraction...")
run_script("feature_extraction.py")
time.sleep(5)

# 3. ML-Based Detection
print("[3/5] Starting ML-based attack detection...")
run_script("live_detection.py")
time.sleep(5)

# 4. Alert Engine
print("[4/5] Starting alert engine...")
run_script("alert_engine.py")
time.sleep(5)

# 5. Traffic Analysis (can be rerun anytime)
print("[5/5] Running traffic analysis...")
run_script("traffic_analysis.py")

print("\n------------------------------------")
print("All IDS components started successfully.")
print("Generate traffic or run nmap to observe:")
print("- ML predictions")
print("- Alerts")
print("- Traffic analysis plots")
print("------------------------------------")
