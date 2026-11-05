import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "network-traffic-anomaly"))

from scapy.all import IP, UDP, Ether, rdpcap, wrpcap  # noqa: E402

import traffic_anomaly as ta  # noqa: E402


def make_capture(path):
    packets = [Ether() / IP(src="192.0.2.10", dst="198.51.100.1") / UDP()] * 600
    packets += [Ether() / IP(src="192.0.2.20", dst="198.51.100.1") / UDP()] * 40
    wrpcap(str(path), packets)


def test_counts_and_flags_heavy_source(tmp_path):
    pcap = tmp_path / "sample.pcap"
    make_capture(pcap)
    counts = ta.count_sources(rdpcap(str(pcap)))
    assert counts["192.0.2.10"] == 600
    assert counts["192.0.2.20"] == 40
    assert ta.find_anomalies(counts, threshold=500) == {"192.0.2.10": 600}


def test_chart_written(tmp_path):
    pcap = tmp_path / "sample.pcap"
    make_capture(pcap)
    counts = ta.count_sources(rdpcap(str(pcap)))
    out = ta.plot_top_talkers(counts, ta.find_anomalies(counts), out=str(tmp_path / "c.png"))
    assert Path(out).stat().st_size > 0
