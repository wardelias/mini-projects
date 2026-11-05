import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ai-funnel-builder"))

from funnel_builder import AIFunnelCreator  # noqa: E402

STAGES = {
    "awareness": {"visitors": 10000},
    "interest": {"visitors": 8500},
    "consideration": {"visitors": 4000},
    "conversion": {"visitors": 600},
    "retention": {"visitors": 450},
}


def make():
    return AIFunnelCreator(client=object())  # no API calls in these tests


def test_conversion_rate():
    assert make().calculate_conversion_rate(STAGES) == 6.0


def test_stage_health():
    metrics = make().calculate_metrics(STAGES)
    assert metrics["interest"]["status"] == "healthy"        # 15% drop
    assert metrics["consideration"]["status"] == "critical"  # 53% drop
    assert metrics["retention"]["status"] == "needs_attention"  # 25% drop


def test_create_and_list():
    app = make()
    app.create_funnel("Spring sale", "ecommerce", STAGES)
    assert "Spring sale" in app.list_funnels()
