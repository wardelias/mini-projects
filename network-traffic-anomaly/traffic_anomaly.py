"""Flag unusually chatty hosts in a packet capture.

Reads a .pcap/.pcapng file, counts IPv4 packets per source address, flags every source
above a threshold, and plots the top talkers with anomalies in red.

    python traffic_anomaly.py capture.pcapng --threshold 500 --top 10 --out chart.png
"""
import argparse
from collections import Counter

DEFAULT_THRESHOLD = 500  # packets; sources above this are flagged


def count_sources(packets):
    """Return a Counter of IPv4 source addresses (ARP and IPv6 are ignored)."""
    from scapy.all import IP

    return Counter(p[IP].src for p in packets if p.haslayer(IP))


def find_anomalies(ip_counts, threshold=DEFAULT_THRESHOLD):
    """Return {ip: count} for every source that sent more than `threshold` packets."""
    return {ip: n for ip, n in ip_counts.items() if n > threshold}


def plot_top_talkers(ip_counts, anomalies, top=10, out="anomaly_graph.png", show=False):
    import matplotlib.pyplot as plt

    top_ips = ip_counts.most_common(top)
    if not top_ips:
        return None
    ips, counts = zip(*top_ips)
    colors = ["#c0392b" if ip in anomalies else "#5dade2" for ip in ips]

    plt.figure(figsize=(10, 6))
    plt.bar(ips, counts, color=colors)
    plt.xlabel("Source IP address")
    plt.ylabel("Packets sent")
    plt.title("Network traffic volume by source (red = anomaly)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    if show:
        plt.show()
    plt.close()
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pcap", help="path to a .pcap or .pcapng file")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                        help=f"packets above which a source is flagged (default {DEFAULT_THRESHOLD})")
    parser.add_argument("--top", type=int, default=10, help="sources to plot (default 10)")
    parser.add_argument("--out", default="anomaly_graph.png", help="chart output path")
    parser.add_argument("--show", action="store_true", help="also open the chart window")
    args = parser.parse_args()

    from scapy.all import rdpcap

    print(f"Loading {args.pcap} ...")
    packets = rdpcap(args.pcap)
    ip_counts = count_sources(packets)
    anomalies = find_anomalies(ip_counts, args.threshold)

    print("\n--- TRAFFIC ANALYSIS REPORT ---")
    print(f"IPv4 packets analysed: {sum(ip_counts.values())}")
    print(f"Distinct sources:      {len(ip_counts)}")
    print(f"\nSources above {args.threshold} packets:")
    if anomalies:
        for ip, n in sorted(anomalies.items(), key=lambda kv: -kv[1]):
            print(f"  [ALERT] {ip} sent {n} packets")
    else:
        print("  none")

    path = plot_top_talkers(ip_counts, anomalies, args.top, args.out, args.show)
    if path:
        print(f"\nChart saved to {path}")


if __name__ == "__main__":
    main()
