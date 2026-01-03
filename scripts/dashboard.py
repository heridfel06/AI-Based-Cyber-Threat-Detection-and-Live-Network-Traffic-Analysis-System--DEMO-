import streamlit as st
import pandas as pd
import os
import time

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALERT_DIR = os.path.join(BASE_DIR, "alerts")

FEATURE_FILE = os.path.join(DATA_DIR, "live_features.csv")
ALERT_FILE = os.path.join(ALERT_DIR, "alerts.log")

st.set_page_config(page_title="AI-Based IDS Dashboard", layout="wide")

st.title("AI-Based Cyber Threat Detection Dashboard")

# -----------------------------
# Auto refresh
# -----------------------------
REFRESH_INTERVAL = 5  # seconds

# -----------------------------
# Load data safely
# -----------------------------
def load_live_features():
    if os.path.exists(FEATURE_FILE):
        return pd.read_csv(FEATURE_FILE)
    return pd.DataFrame()

def load_alerts():
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            lines = f.readlines()
        return pd.DataFrame({"Alert Log": lines})
    return pd.DataFrame()

# -----------------------------
# Dashboard layout
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Live Traffic Features")
    df_features = load_live_features()
    if not df_features.empty:
        st.dataframe(df_features.tail(10), use_container_width=True)
        st.metric("Total Feature Windows", len(df_features))
    else:
        st.info("Waiting for live features...")

with col2:
    st.subheader("Recent Alerts")
    df_alerts = load_alerts()
    if not df_alerts.empty:
        st.dataframe(df_alerts.tail(10), use_container_width=True)
        st.metric("Total Alerts", len(df_alerts))
    else:
        st.success("No alerts detected")

# -----------------------------
# Traffic statistics
# -----------------------------
st.subheader("Traffic Statistics")

if not df_features.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("Unique Source IPs", df_features["src_ip"].nunique())
    c2.metric("Average Packet Count", round(df_features["packet_count"].mean(), 2))
    c3.metric("Average Flow Duration", round(df_features["flow_duration"].mean(), 2))

# -----------------------------
# Footer
# -----------------------------
st.caption("Real-time IDS monitoring using Machine Learning and Anomaly Detection")

time.sleep(REFRESH_INTERVAL)
st.rerun()
