# Track 3 · Operator

This is the track most public LLM roadmaps skip. The scientist trains.
The engineer ships a product. Someone still has to keep a model answering
under a latency budget, on a GPU bill that does not surprise finance, with
logs that a lawyer can defend.

If you run a gateway, a GPU box, or an OpenAI-compatible endpoint for other
teams, start here. If you only call a vendor API, still read O2 and O3:
timeouts and token economics do not care who owns the weights.

| Order | File | Lab |
|---|---|---|
| O1 | [Serving engines](01-serving-engines.md) | 15, then 18 |
| O2 | [Reliability](02-reliability.md) | 15 against a local runtime if you have one |
| O3 | [Cost and capacity](03-cost-and-capacity.md) | 13, 19 |
| O4 | [Observability](04-observability.md) | 12, then re-read E10 |

When O3 is easy, you can talk to a leader about budget without guessing.
When O4 is easy, an incident has a trace instead of a Slack anecdote.

Do not start this track if you cannot yet explain a token, a KV cache, and
why decode is often memory-bound. Those are [F5](../00-fundamentals/05-scaling-and-hardware.md)
and [E6](../02-engineer/06-inference-optimization.md). This track assumes
them.

Companion reading sits in [reference/TOOLS.md](../../reference/TOOLS.md).
This track names engines so you can choose. It does not paste vendor
quickstarts.
