# ADR-0001: Job orchestration — start with Celery+Redis behind an interface

- **Date:** 2026-06-16
- **Status:** Accepted
- **Deciders:** Nitin

## Context
The analysis pipeline is slow (depth + segmentation + a diffusion render = tens of
seconds to minutes), GPU-bound, bursty, and multi-step with partial failures. It cannot
run synchronously inside an HTTP request — the request would time out and a mid-pipeline
crash would lose all progress. We are a solo developer on a ~$20–50/mo budget who wants
to *learn* the concepts, not just adopt the heaviest tool. So we need asynchronous,
resumable background execution — but proportionate to the stage we're at.

## Decision
Use **Celery + Redis** for background jobs in v1, but put it **behind a thin
`JobRunner` interface** (`submit()`, `get_status()`, `stream_events()`) so the rest of
the codebase never imports Celery directly. This makes a later swap to a durable
workflow engine a one-file change, not a refactor.

## Alternatives considered
- **Temporal now** — durable execution, automatic per-activity retries, human-in-the-loop
  interrupts, replayable history. Genuinely the right *production* tool and where we'll
  likely land in Phase 9. **Rejected for v1:** it adds a server + worker + its own mental
  model to operate and pay for, which is overkill while we're still learning the pipeline.
  Adopting it now would be choosing infrastructure before understanding the load — a
  classic over-engineering trap.
- **Run synchronously in the request** — simplest possible. **Rejected:** GPU steps will
  blow past HTTP timeouts and any crash loses the whole job. Non-starter for this workload.
- **Cloud-native queue (SQS) + plain workers** — cheap and managed. **Rejected for v1:**
  couples local dev to cloud and gives us less local control while learning; revisit at
  deploy time.

## Consequences
- **Positive:** dead-simple local setup (`docker-compose` brings up Redis), a well-trodden
  Python path, and we genuinely learn the queue/worker/result-backend model by hand.
- **Negative / cost:** Celery does not give true durable execution or first-class
  human-in-the-loop interrupts — we'll hand-roll idempotency and a status row in Postgres.
  Some of that work is effectively re-implementing a slice of Temporal.
- **Revisit when:** we add human-in-the-loop steps, need replayable history for debugging,
  or move to multi-step workflows with many failure points — i.e. Phase 6/9. The
  `JobRunner` interface is what makes that revisit cheap.
