# ADR-0001: Separate Batch and Live Monitoring Modes

**Status:** Accepted
**Decision scope:** Log monitoring execution model

## Context

The initial log monitoring implementation used an infinite polling loop and positioned the file cursor at EOF.

This design supported continuous monitoring but did not provide a straightforward way to analyze historical entries or execute deterministic tests.

During QA, the process appeared to hang because it waited indefinitely for newly appended data.

The application required distinct execution behaviors for historical analysis and continuous monitoring.

## Decision

Implement two execution modes through the `live` parameter and command-line `--live` flag.

**Batch mode:**
- Starts at the beginning of the file.
- Processes existing entries.
- Exits at EOF.
- Supports deterministic automated tests.

**Live mode:**
- Starts at EOF.
- Processes newly appended entries.
- Polls periodically for new data.
- Continues until interrupted.

Both modes reuse the same `analyze_line()` detection function.

## Alternatives Considered

### 1. Continuous monitoring only

**Rejected:** Difficult to test historical data and unsuitable for finite batch processing.

### 2. Separate scripts for batch and live monitoring

**Not selected:** Would introduce unnecessary duplication at the current project scale.

### 3. Single implementation with configurable execution mode

**Selected:** Provides distinct runtime behavior while reusing detection logic.

## Consequences

### Benefits

- Improved testability.
- Predictable batch execution.
- Reduced duplication.
- Clearer CLI behavior.
- Reusable detection logic.

### Tradeoffs

- Two execution paths require validation.
- Polling introduces a detection delay.
- Live mode requires explicit termination.
- File rotation and truncation remain unsupported.

## Validation

The decision was validated through automated batch-processing tests and manual live-monitoring verification.

The automated test suite completed with 14 passing tests.

## Revisit Conditions

Reevaluate this decision if the application requires multiple concurrent log sources, durable offsets, event streaming, or asynchronous ingestion.