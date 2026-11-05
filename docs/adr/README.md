# Architecture Decision Records

This directory records significant architectural decisions affecting the Security Log Monitor.

ADRs document the context, alternatives, decision, consequences, and conditions under which a decision should be revisited.

## Decision Register

| ID | Decision | Status |
|---|---|---|
| [ADR-0001](0001-batch-live-modes.md) | Separate Batch and Live Monitoring Modes | Accepted |

## Conventions

- Use sequential numbering.
- Record one architectural decision per ADR.
- Preserve accepted decisions for historical traceability.
- Supersede outdated decisions rather than silently rewriting their history.
- Link relevant ADRs from architecture documents and implementation changes.

## Future Decision Candidates

- Structured event schema selection.
- File rotation and checkpoint strategy.
- Polling versus event-driven ingestion.
- Alert output and persistence design.
- Security response approval architecture.