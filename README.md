# Security Log Monitoring & Detection

Python Security Automation Lab | Detection Engineering | MVP

## Overview

A Python-based security log monitoring utility designed to identify configurable indicators of interest within application and system log files.

The  implementation supports historical log analysis and continuous monitoring of newly appended log entries. It provides a command-line interface, reusable detection logic, and automated tests.

This project represents an initial implementation within a broader security automation engineering portfolio. Development emphasizes modular architecture, predictable execution, testability, operational safeguards, and iterative improvements toward production-grade reliability.

 Current maturity: Functional MVP — core behavior validated through automated and manual testing.

## Technical Documentation

- [System Architecture](docs/architecture.md)
- [Testing Strategy](docs/testing-strategy.md)
- [Engineering Roadmap](docs/roadmap.md)
- [Architecture Decision Records](docs/adr/README.md)

## Engineering Objectives

- Implement reusable log analysis functions independent of the execution interface.
- Support both historical analysis and continuous event monitoring.
- Detect predefined log severity indicators using compiled regular expressions.
- Provide deterministic execution and clear termination behavior.
- Validate inputs and handle expected file access errors.
- Establish automated regression tests before expanding functionality.
- Document design limitations and planned reliability improvements.

## Architecture

The current implementation separates log evaluation from file monitoring and command-line orchestration.

### System Data Flow

```text
Command-Line Interface
         |
         v
Input Validation
         |
         v
Log File Reader
         |
         v
Regex Detection Engine
         |
         v
Alert Output / Metrics
```

### Core Components

| Component | Responsibility |
|---|---|
| `analyze_line()` | Evaluates a log entry against predefined detection patterns |
| `monitor_logs()` | Reads historical or newly appended log entries |
| `argparse` | Processes command-line arguments |
| `pathlib` | Handles filesystem paths and file validation |
| `re` | Provides compiled, case-insensitive pattern matching |
| `pytest` | Validates detection and file-processing behavior through automated tests |

### Execution Modes

**Batch Mode**

Processes existing log entries, identifies matching events, reports findings, and exits at the end of the file.

**Live Mode**

Begins monitoring at the end of the file, detects newly appended entries, and continues until interrupted by the user.

### Architectural Principles

- **Separation of concerns:** Detection logic is separated from file reading and command-line handling at the function level.
- **Testability:** Detection behavior can be validated independently using deterministic test inputs.
- **Safe execution:** The monitor reads source logs without modifying them or executing response actions.
- **Operational visibility:** Matching events and total alert counts are reported through the console.
- **Incremental maturity:** The implementation will evolve toward modular components, structured events, and improved reliability.

### Detailed Engineering Documentation

- [System Architecture](docs/architecture.md)
- [Testing Strategy](docs/testing-strategy.md)
- [Engineering Roadmap](docs/roadmap.md)
- [Architecture Decision Records](docs/adr/README.md)

## Functional Capabilities

### Historical Analysis

Batch mode reads existing log entries, identifies matches, reports findings, and exits.

```bash
python monitor_log_entries.py data/sample_auth.txt
```

### Continuous Monitoring

Live mode begins at the end of the log file and processes newly appended entries.

```bash
python monitor_log_entries.py data/sample_auth.txt --live
```

Terminate live monitoring using `Ctrl+C`.

### Detection Logic

The MVP identifies standalone `ERROR` and `WARNING` tokens using a compiled regular expression with case-insensitive matching.

Detection is intentionally simple and deterministic. It should not be interpreted as behavioral threat detection or confirmation of malicious activity.

## Testing and Quality Assurance

The project uses pytest for automated verification of core functionality.

Latest verified automated test result: 14 passed, 0 failed, 0 errors.

Test coverage includes:

- Positive detection of warning and error indicators.
- Case-insensitive detection.
- Exclusion of ordinary informational and debugging entries.
- Regular-expression boundary behavior.
- Historical log processing.
- Missing-file exception handling.
- Empty-file processing.

### Manual Integration Testing

Live monitoring was validated by starting the application, appending synthetic log entries from a separate terminal, and confirming that newly appended warning and error entries generated alerts.

The process also terminated gracefully through keyboard interruption and reported the expected alert count.

### Testing Limitations

Automated tests ly focus on batch processing and detection behavior. Live-mode behavior has been manually verified but is not yet covered by an automated integration test.

Statement coverage and branch coverage have not yet been measured.

## Sample Security Events

The repository includes a synthetic authentication log containing normal activity, failed authentication attempts, and simulated security-relevant events.

The sample dataset supports repeatable demonstrations of historical log processing.

Run:

```bash
python monitor_log_entries.py data/sample_auth.txt
```

The monitor evaluates each log entry against its configured severity patterns and reports matching `WARNING` and `ERROR` entries.

**Note:** The current implementation performs keyword-based detection. It does not independently verify malicious activity, identify attackers, or correlate authentication events.

## Security and Operational Considerations

### Input Trust

Log entries are treated as untrusted data. The  application performs keyword detection without executing content from log messages.

### File Access

The application validates that the requested file exists before processing it.

### Execution Safety

The utility is read-only with respect to the monitored log file. It does not modify source logs or execute containment actions.

### Data Handling

Testing uses synthetic log data. Sensitive operational logs, credentials, and generated runtime artifacts should not be committed to the repository.

## Known Limitations

| Area | Current limitation | Planned improvement |
| :--- | :--- | :--- |
| Detection | Keyword-based severity | Structured log parsing and security-specific detection rules |
| Log lifecycle | No log rotation or truncation handling | Rotation-aware file monitoring |
| Input formats | Plain-text log files | Structured JSON and additional log formats |
| Output | Console-based alerts | Structured JSON events and persistent audit records |
| Observability | Basic alert count | Processing metrics, latency, and error telemetry |
| Reliability | No checkpoint persistence | Durable offsets and recovery behavior |
| Configuration | Detection pattern defined in code | Externalized and validated configuration |
| Testing | Limited automated integration coverage | Integration, failure-injection, and performance tests |

## Engineering Roadmap

### Phase 1 — Functional MVP

- [x] Implement historical log analysis.
- [x] Implement continuous monitoring.
- [x] Add reusable detection logic.
- [x] Add CLI argument parsing.
- [x] Implement input validation.
- [x] Establish automated tests.
- [x] Validate live monitoring manually.

### Phase 2 — Reliability and Modularization

- [ ] Separate ingestion, detection, and reporting into dedicated modules.
- [ ] Introduce structured event schemas.
- [ ] Implement log rotation and truncation handling.
- [ ] Add persistent processing checkpoints.
- [ ] Improve exception handling and diagnostic logging.
- [ ] Expand automated integration testing.

### Phase 3 — Security Operations Integration

- [ ] Introduce configurable detection rules.
- [ ] Support event enrichment and correlation.
- [ ] Integrate with an alert ingestion pipeline.
- [ ] Add controlled response recommendations.
- [ ] Record response outcomes and operational metrics.

### Phase 4 — Production Readiness Evaluation

- [ ] Implement performance and load testing.
- [ ] Establish deployment and runtime configuration controls.
- [ ] Add CI quality gates and dependency scanning.
- [ ] Validate recovery behavior under failure conditions.
- [ ] Define operational service objectives.
- [ ] Conduct security review and document residual risks.

## Engineering Principles

This project is developed around five principles:

1. Separation of concerns: Detection logic should remain independent of input and presentation layers.
2. Testability: Components should be independently verifiable with deterministic inputs.
3. Safe defaults: Security automation should minimize unintended operational effects.
4. Observability: Execution behavior and failures should be measurable and explainable.
5. Incremental maturity: Production readiness must be demonstrated through evidence, not assumed from feature completion.

## Project Status

Functional MVP validated. Production hardening in progress.

This repository documents an iterative engineering process, including implementation, testing, architectural refinement, and operational improvements.
