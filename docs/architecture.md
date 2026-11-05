# System Architecture — Security Log Monitor

**Status:** MVP implemented
**Architecture version:** 0.1
**Scope:** Local file-based security log monitoring

## 1. Architectural Overview

The Security Log Monitor is a Python command-line application supporting historical and continuous log analysis.

The system uses a lightweight, synchronous architecture that separates command-line input handling, filesystem access, pattern evaluation, and alert reporting.

The current implementation does not depend on external APIs, cloud services, databases, or privileged system operations.

## 2. Component Architecture

```text
                    CLI
                     |
               argparse
                     |
                     v
              monitor_logs()
                     |
              Path Validation
                     |
                     v
               File Reader
                /        \
          Batch Mode    Live Mode
          Read to EOF   Seek to EOF
                \        /
                 v      v
                analyze_line()
                     |
              Compiled Regex
                     |
                Match?
                /    \
              No      Yes
              |        |
            Skip     Print Alert
                       |
                 Increment Count
```

## 3. Component Responsibilities

| Component | Responsibility |
|---|---|
| CLI | Accept log path and execution mode |
| File validation | Confirm the input is an existing file |
| File reader | Retrieve log entries sequentially |
| Detection engine | Identify predefined severity indicators |
| Alert reporting | Print matching events and track alert counts |
| Shutdown handling | Respond to user interruption |

## 4. Execution Modes

### Batch Mode

The application begins reading at the start of the file, evaluates each entry, and exits at EOF.

### Live Mode

The application moves the file cursor to EOF, polls for newly appended entries, and continues until interrupted.

The current implementation uses a 0.5-second polling interval.

## 5. Data Contracts

**Input:** Path to a readable, plain-text log file.

**Detection function:** `analyze_line(line: str) -> bool`

**Monitoring function:** `monitor_logs(log_file, live=False) -> int`

**Output:** Console alerts and the number of matching log entries.

The monitoring function currently reports matches rather than producing structured event objects.

## 6. Security Boundaries

- Log content is treated as untrusted input.
- No log content is executed as code.
- The monitored file is opened in read-only mode.
- The application does not modify security controls or perform containment.
- Log content is printed to the console and may contain sensitive information; production deployment will require output sanitization and data-handling controls.

## 7. Architectural Constraints

- Single-process, synchronous execution.
- Polling-based monitoring.
- No durable processing checkpoint.
- No log rotation handling.
- No persistent alert storage.
- No event correlation or threat intelligence integration.

## 8. Future Architecture

The planned architecture separates ingestion, detection, enrichment, response, and observability into independently testable modules.

These components are not part of the current MVP and will be introduced incrementally.

## 9. Related Decisions

- [ADR-0001: Separate Batch and Live Monitoring Modes](adr/0001-batch-live-modes.md)