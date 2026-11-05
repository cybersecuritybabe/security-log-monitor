# Testing Strategy — Security Log Monitor

**Status:** Initial QA completed
**Framework:** pytest

## 1. Testing Objectives

Verify that the log monitoring application:

- Correctly identifies configured log severity indicators.
- Avoids specified false-positive substring matches.
- Handles valid and invalid file inputs.
- Processes historical logs deterministically.
- Detects newly appended log entries.
- Exits gracefully when interrupted.

## 2. Test Levels

| Level | Scope | Current status |
|---|---|---|
| Unit | Regex detection and boundary cases | Passed |
| Functional | Batch processing and file validation | Passed |
| Manual integration | Live monitoring and shutdown | Passed |
| Automated integration | Live monitoring lifecycle | Planned |
| Performance | Large files and sustained event throughput | Planned |
| Resilience | Rotation, truncation, encoding and filesystem failures | Planned |

## 3. Verified Test Evidence

### Automated Testing

Command:

`python -m pytest -v`

Last verified result:

**14 passed, 0 failed, 0 errors.**

Validated scenarios include case-insensitive detection, regex boundaries, existing log processing, empty files, and nonexistent files.

### Manual Integration Testing

Live monitoring was started using the `--live` argument.

Synthetic `WARNING` and `ERROR` entries were appended to the monitored file from another terminal.

Both entries generated alerts. The application exited after Ctrl+C and reported two detected alerts.

## 4. Acceptance Criteria

The current MVP is considered functionally validated when:

1. All automated tests pass.
2. Batch mode processes existing entries and terminates.
3. Live mode detects newly appended matching entries.
4. User interruption terminates monitoring gracefully.
5. The final alert count matches observed detections.

## 5. Known Coverage Gaps

- No automated test for continuous monitoring.
- No test for file rotation or truncation.
- No test for permission errors during file access.
- No measured code or branch coverage.
- No performance benchmark.
- No validated recovery mechanism after interruption.

## 6. Future Quality Gates

Planned quality gates include:

- Automated pytest execution in CI.
- Static analysis and formatting checks.
- Dependency and secret scanning.
- Coverage reporting.
- Integration tests for file lifecycle events.
- Performance and reliability acceptance thresholds.

Passing the existing test suite does not establish production readiness.