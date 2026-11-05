# AI Funnel Builder

An interactive command-line assistant for designing and analysing marketing funnels. You
enter visitor counts for each stage; it computes overall conversion and per-stage drop-off,
labels each stage's health, and asks Claude for bottlenecks and fixes.

## Usage

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key
python funnel_builder.py
```

Commands inside the session:

| Command | Action |
|---|---|
| `create` | define a funnel: name, type, visitors per stage |
| `list` | show saved funnels with conversion rates |
| `analyze` | send a funnel's metrics to Claude for a bottleneck analysis |
| `ask` | free-form question; the conversation keeps context |
| `exit` | quit |

## Funnel model

Stages: awareness → interest → consideration → conversion → retention.

- **Conversion rate** = conversion visitors ÷ awareness visitors.
- **Drop-off** per stage = 1 − visitors ÷ previous stage's visitors.
- **Health**: under 20% drop-off is *healthy*, 20–40% *needs attention*, above 40%
  *critical*.

The metric logic is plain Python and is unit-tested without calling the API; the Claude
client is injectable (`AIFunnelCreator(client=...)`).
