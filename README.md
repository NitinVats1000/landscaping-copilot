# AI Landscaping Copilot

Upload a photo of an outdoor garden and get back **measured** plantable area, a
**computed** sun-exposure read, plant recommendations **with a why-breakdown**, a
**geometry-faithful "after" render**, and a costed bill of materials — all traceable
to the photo.

> **Not a GPT wrapper.** The moat is grounding: segmentation + *metric* depth produce
> real m² and computed sun-hours; a structured horticultural knowledge base makes
> recommendations auditable; and the render is generated *downstream of* the bill of
> materials, so the picture and the plan never diverge.

## Status

🚧 **In active development** — building a portfolio-grade vertical slice end-to-end.
See the docs below for the live architecture, scope, non-functional targets, and
decision records.

## Architecture at a glance

- **Vision:** scene → SAM-class segmentation → metric depth → plant ID → spatial reasoning → `SiteModel`
- **Intelligence:** deterministic suitability scorer over a plant knowledge base (this produces the "why")
- **Generation:** FLUX.1 depth/fill + ControlNet, mask-constrained and species-faithful
- **Orchestration:** LangGraph agents behind a durable, swappable job runner

## Docs

- [`docs/01-scope-v1.md`](docs/01-scope-v1.md) — what's in v1 and what's deliberately deferred
- [`docs/02-non-functionals.md`](docs/02-non-functionals.md) — latency, cost, and accuracy targets (derived, not asserted)
- [`docs/contracts/site_model.py`](docs/contracts/site_model.py) — the data contract at the system's spine
- [`docs/adr/`](docs/adr/) — architecture decision records (the "why X not Y" trail)
- [`docs/architecture/`](docs/architecture/) — C4 container view and data-flow diagrams

## Key design principles

- **Vertical slice over broad coverage** — ship one path through every layer, then deepen
- **Measured, not guessed** — real m² and computed sun-hours, with confidence on every inferred value
- **Hosted-API-first, open-source where the moat lives** — learn fast, stay cheap, own what matters
- **Plan and visualization are coupled** — renders are downstream of the bill of materials

## Tech

Python · FastAPI · Pydantic v2 · LangGraph · PostgreSQL + pgvector · Celery/Redis · Docker

## License

MIT
