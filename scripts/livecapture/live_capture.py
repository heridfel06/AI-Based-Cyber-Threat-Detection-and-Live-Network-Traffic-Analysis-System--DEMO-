# live_capture.py
# Usage examples (run as Admin):
# python live_capture.py --iface 1 --count 200 --save packets.csv
# python live_capture.py --iface 1 --display_filter "dns || http" --save packets.csv --timeout 30

import argparse, time, csv, sys
import pyshark

parser = argparse.ArgumentParser()
parser.add_argument('--iface', required=True, help="Interface id or name (use: tshark -D)")
parser.add_argument('--count', type=int, default=0, help="Stop after N packets (0 = unlimited)")
parser.add_argument('--timeout', type=int, default=0, help="Stop after N seconds (0 = unlimited)")
parser.add_argument('--display_filter', type=str, default="", help="Wireshark display filter (e.g., dns || http)")
parser.add_argument('--only_syn', action='store_true', help="Print only TCP SYN packets")
parser.add_argument('--save', type=str, default="packets.csv", help="Save parsed packets to CSV file")
args = parser.parse_args()

iface = str(args.iface)
cap_kwargs = {'interface': iface}
if args.display_filter:
    cap_kwargs['display_filter'] = args.display_filter

cap = pyshark.LiveCapture(**cap_kwargs)
print(f"Starting capture on {iface} (count={args.count}, timeout={args.timeout}, filter='{args.display_filter}')")
start_time = time.time()
seen = 0

csv_file = open(args.save, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['idx','ts','proto','src','sport','dst','dport','length','info'])

try:
    for pkt in cap.sniff_continuously():
        seen += 1
        if args.count and seen > args.count:
            break
        if args.timeout and (time.time() - start_time) > args.timeout:
            break

        try:
            ts = getattr(pkt, 'sniff_timestamp', time.time())
            proto = pkt.transport_layer or pkt.highest_layer or 'N/A'
            src = getattr(getattr(pkt, 'ip', None), 'src', 'N/A')
            dst = getattr(getattr(pkt, 'ip', None), 'dst', 'N/A')
            length = getattr(pkt, 'length', 'N/A')

            sport = dport = ''
            if pkt.transport_layer:
                tl = pkt.transport_layer.lower()
                try:
                    sport = getattr(getattr(pkt, tl), 'srcport', '')
                    dport = getattr(getattr(pkt, tl), 'dstport', '')
                except Exception:
                    sport = dport = ''

            if args.only_syn:
                if proto != 'TCP':
                    continue
                try:
                    flags = int(getattr(pkt.tcp, 'flags', 0))
                    SYN_MASK = 0x02
                    if not (flags & SYN_MASK):
                        continue
                except Exception:
                    continue

            info = getattr(pkt, 'info', '')
            print(f"{seen:5d} {proto:6} {src:21} -> {dst:21} sport={sport:6} dport={dport:6} len={length}")
            csv_writer.writerow([seen, ts, proto, src, sport, dst, dport, length, info])
            csv_file.flush()
        except KeyboardInterrupt:
            raise
        except Exception:
            continue

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C).")

finally:
    try:
        cap.close()
    except Exception:
        pass
    csv_file.close()
    print(f"Capture finished. Packets seen: {seen}")
    sys.exit(0)
