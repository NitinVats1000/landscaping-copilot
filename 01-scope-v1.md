# v1 Scope — the cut

> The single most valuable decision in this whole project. v1 is a **vertical slice**:
> the thinnest path that touches every architectural layer end-to-end and is deployable.
> If a feature does not strengthen that one path, it is deferred — not cancelled, deferred.

## The one-sentence product (v1)
"Upload a photo of an outdoor home garden and get back **measured** plantable area,
a **computed** sun exposure read, **plant recommendations with a why-breakdown**, **one
faithful 'after' render**, and a **costed bill of materials** — all traceable to the photo."

## IN scope (v1)
- Environment: **outdoor home gardens only**
- Input: **single uploaded photo** (+ EXIF if present)
- Models: **hosted-API-first** (cheap, fast to learn)
- Capabilities:
  - Scene understanding (is it a garden? what's in it?)
  - Segmentation of **empty plantable space** + **existing plants**
  - **Rough metric** dimension estimate (m²) — honest about uncertainty
  - **Computed** sun-class (full/part/shade) from orientation + geometry
  - Plant recommendation **with a per-factor score breakdown** (the "why")
  - **One** faithful design render (depth + mask constrained)
  - Bill of materials + cost estimate
- Agents: **3** (Site Analysis, Plant Recommendation, Cost) — not 7

## OUT of scope (v2 hooks only — leave notes, not code)
indoor / balcony / commercial · AR · growth / seasonal / disease / carbon / heat
simulations · nursery inventory integration · compliance gate · multi-style design ·
the full 7-agent graph · self-hosted GPU inference · per-species LoRAs · Neo4j graph

## The "a-wrapper-can't-do-this" capability
**Computed sun-class + real m².** A VLM hallucinates "looks like it gets good light."
We *compute* sun-hours from latitude + date + scene geometry and *measure* area from
metric depth. That is the demo moment and the interview headline.

## Non-goals (explicitly NOT trying to do, ever, in v1)
- Be accurate to the centimetre (we target "useful estimate + stated confidence")
- Cover every species (we seed ~200 commercially relevant ones)
- Look like a finished consumer app (portfolio-grade, not pixel-perfect)
