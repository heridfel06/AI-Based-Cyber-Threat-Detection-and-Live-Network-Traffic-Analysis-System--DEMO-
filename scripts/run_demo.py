import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

RUNTIME_SCRIPTS = [
    "live_capture.py",
    "feature_extraction.py",
    "live_detection.py",
    "live_anomaly_detection.py",
    "alert_engine.py",
    "auto_response.py"
]

def run_script(script):
    path = os.path.join(SCRIPTS_DIR, script)
    print(f"▶ Starting {script}")
    return subprocess.Popen(
        [sys.executable, path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

print("=" * 60)
print(" AI-BASED IDS – FULL RUNTIME DEMO ")
print("=" * 60)

print("\nRuntime services to be launched:")
for s in RUNTIME_SCRIPTS:
    print(f"  • {s}")

print("\nNOTE:")
print("• Training scripts are NOT launched (already completed)")
print("• Dashboard is started manually")
print("• Some services remain silent until events occur\n")

processes = []

for script in RUNTIME_SCRIPTS:
    processes.append(run_script(script))
    time.sleep(4)

print("\n================================================")
print(" ALL RUNTIME IDS SERVICES ARE NOW RUNNING ")
print("================================================")

print("\nWHAT TO EXPECT:")
print("• live_capture.py → packet logs")
print("• feature_extraction.py → CSV updates")
print("• live_detection.py → ML output")
print("• live_anomaly_detection.py → anomaly scores")
print("• alert_engine.py → alerts.log")
print("• auto_response.py → response.log")

print("\nOPTIONAL:")
print("Start dashboard manually:")
print("python -m streamlit run dashboard.py")

print("\nSTOP:")
print("Close individual windows or press CTRL+C inside them.")
