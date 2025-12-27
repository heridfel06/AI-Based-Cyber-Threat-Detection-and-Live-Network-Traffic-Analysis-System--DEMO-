AI-Based Cyber Threat Detection and Live Network Traffic Analysis System
1. Project Overview

This project implements a real-time Intrusion Detection System (IDS) that captures live network traffic, extracts flow-based features, and detects cyber threats using a machine learning model.

The system combines:

Live packet capture

Feature extraction

Supervised machine learning (Random Forest)

Rule-based alerting

Traffic visualization

The objective is to demonstrate how AI techniques can be applied to real network traffic for cyber threat detection in an academic setting.

2. Problem Statement

Traditional security systems rely heavily on static rules and signatures, which are ineffective against evolving cyber attacks.

This project addresses the problem by:

Monitoring live network traffic

Learning attack patterns from historical datasets

Detecting anomalies and malicious behavior in real time

Generating alerts with explainable reasons

3. System Architecture

The system follows a modular pipeline architecture:

Live Packet Capture

Feature Extraction

Offline Dataset Preparation

ML Model Training

Live ML-Based Detection

Alert Generation

Traffic Analysis and Visualization

Each module operates independently but integrates into a single IDS workflow.

4. Technologies Used
Programming Language

Python 3.9+

Libraries

Scapy – Live packet capture

Pandas, NumPy – Data processing

Scikit-learn – Machine learning

Matplotlib – Visualization

Joblib – Model persistence

Dataset

NSL-KDD Dataset (offline training)

Platform

Windows OS


6. Feature Description
Live Traffic Features

Packet count

Unique destination ports

Average packet size

TCP flag

UDP flag

Flow duration

These features are aggregated over time windows and used for ML inference.

7. Machine Learning Model

Algorithm: Random Forest Classifier

Type: Supervised binary classification

Classes:

0 → Normal Traffic

1 → Attack Traffic

Evaluation Metrics

Accuracy

Precision

Recall

Confusion Matrix

The trained model is saved and reused for real-time detection.

8. Alert Generation Logic

Alerts are generated when:

The ML model predicts an attack

Rule-based threshold detects abnormal behavior (e.g., port scan)

Each alert includes:

Timestamp

Source IP

Detection reason

Alerts are logged to a persistent file for auditing.

9. Traffic Analysis and Visualization

The system generates:

Traffic volume vs time

Protocol distribution

Top source IPs by packet count

Plots are saved for reporting and demonstration purposes.

10. How to Run the Project
Step 1: Activate Virtual Environment
venv\Scripts\activate

Step 2: Run Full Demo (Recommended)
python project/scripts/run_demo.py


This launches:

Live capture

Feature extraction

ML detection

Alert engine

Traffic analysis

Step 3: Generate Traffic

Browse websites

Use ping

Use nmap for testing

11. Testing and Validation
Normal Traffic

No or minimal alerts

Correct classification as NORMAL

Attack Simulation

Port scanning triggers alerts

ML model flags suspicious traffic

Observations

Some false positives may occur

Dataset mismatch and short time windows are known limitations

12. Limitations

Binary classification only (Normal vs Attack)

Dataset trained on offline data

Limited protocol-level inspection

Not designed for high-throughput enterprise networks

13. Future Enhancements

Multi-class attack classification

Deep learning models

Automated mitigation actions

Dashboard-based visualization

Distributed traffic monitoring

14. Conclusion

This project demonstrates a complete AI-based IDS pipeline, integrating live network monitoring with machine learning–based threat detection.


It successfully proves the feasibility of applying ML techniques to real-time cybersecurity monitoring in an academic environment.

