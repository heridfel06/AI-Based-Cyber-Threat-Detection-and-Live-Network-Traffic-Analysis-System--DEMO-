# live_infer.py
import time, argparse, joblib, pandas as pd
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--packets', required=True)
parser.add_argument('--model', required=True)
parser.add_argument('--window', type=int, default=5)
parser.add_argument('--poll', type=float, default=1.0)
args = parser.parse_args()

model = joblib.load(args.model)

print("Monitoring", args.packets, "window", args.window, "s")
try:
    while True:
        try:
            df = pd.read_csv(args.packets)
        except Exception:
            time.sleep(args.poll)
            continue
        if df.empty:
            time.sleep(args.poll)
            continue
        df['ts'] = df['ts'].astype(float)
        max_ts = df['ts'].max()
        start_ts = max_ts - args.window
        w = df[(df['ts'] > start_ts) & (df['ts'] <= max_ts)]
        total = len(w)
        total_bytes = w['length'].apply(pd.to_numeric, errors='coerce').fillna(0).sum()
        tcp_count = (w['proto'] == 'TCP').sum()
        udp_count = (w['proto'] == 'UDP').sum()
        unique_src = w['src'].nunique()
        syn_count = w['info'].astype(str).str.contains('SYN', case=False).sum()
        avg_pkt_len = total_bytes / total if total>0 else 0
        pkt_rate = total / args.window
        feat = [total, total_bytes, tcp_count, udp_count, unique_src, syn_count, avg_pkt_len, pkt_rate]
        pred = model.predict([feat])[0]
        ts_readable = datetime.fromtimestamp(max_ts).strftime('%H:%M:%S')
        print(f"[{ts_readable}] total={total} syn={syn_count} pkt_rate={pkt_rate:.1f} -> pred={pred}")
        if pred == 1:
            print("!!! ALERT: Attack predicted !!!")
        time.sleep(args.poll)
except KeyboardInterrupt:
    print("\nStopped by user.")
