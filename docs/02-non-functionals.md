# Non-Functional Requirements (v1 targets)

> Functional = *what* it does. Non-functional = *how well*. These numbers are the
> guardrails every later decision is checked against. The cost line is the one that
> keeps us inside a $20–50/mo budget — treat it as a hard constraint, not a wish.

## Performance / latency (budgets, not guarantees)
| Stage | Target | Why this number |
|---|---|---|
| Presigned upload + job accept | < 500 ms | It's just a DB write + enqueue; must feel instant |
| Vision pipeline → SiteModel | < 45 s | Hosted depth + segmentation; user sees streamed progress |
| Recommendation + cost | < 10 s | Deterministic scorer + 1 LLM narration call |
| Single render | < 60 s | Diffusion is the slow part; one render, not many |
| **End-to-end (perceived)** | **< 90 s with streaming** | We stream partials so it never feels like a 90s wall |

## Cost (the budget guardrail)
| Item | Target | Lever |
|---|---|---|
| **Cost per full analysis** | **< $0.50** | The whole architecture bends to protect this |
| Render cache hit rate | > 60% after warm-up | Same scene + same plan = reuse image (biggest saver) |
| Idle GPU spend | **$0** | GPU is on-demand / scale-to-zero, never always-on |
| Monthly infra (dev) | < $50 | Free/cheap tiers; hosted models pay-per-call |

## Accuracy (honest, measurable targets — used as eval gates in Phase 7)
| Signal | Target | Metric |
|---|---|---|
| Empty-space segmentation | IoU > 0.70 | vs hand-labeled masks |
| Area estimate | within ±25% | vs tape-measure ground truth on a test set |
| Plant ID (existing) | top-5 > 0.80 | on a held-out garden set |
| Sun-class | correct bucket > 0.75 | vs manual sun-survey labels |
| Render faithfulness | species present & geometry intact | human rubric (Phase 7) |

## Reliability & availability
- v1 target availability: **best-effort** (it's a portfolio project, not a bank)
- Every job is **idempotent and resumable** — a worker crash never corrupts state
- Graceful degradation: if depth fails, still return scene + recs with a confidence note

## Security (baseline — expanded in Phase 9)
- All uploads via **presigned URLs** (no image bytes through the API)
- AuthN on every mutating endpoint; uploads scoped per project
- No secrets in code; `.env` + secret manager; **never** log image URLs with tokens
- PII awareness: photos can contain houses/people — treat as sensitive, short retention

## Observability (built in from Phase 3, not bolted on)
- Structured JSON logs with a `job_id` correlation ID through every stage
- A trace per job (which node ran, how long, what it cost)
- Cost counter per job (tokens + GPU-seconds + API calls)
