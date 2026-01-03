import pandas as pd
import os
import joblib
from sklearn.ensemble import IsolationForest

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

INPUT_FILE = os.path.join(DATA_DIR, "training_dataset.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "anomaly_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE)

# Use ONLY normal traffic
normal_df = df[df["label"] == 0].drop("label", axis=1)

# -----------------------------
# Train Isolation Forest
# -----------------------------
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(normal_df)

# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, MODEL_FILE)

print("PHASE 4A completed successfully.")
print(f"Anomaly model saved at:\n{MODEL_FILE}")
