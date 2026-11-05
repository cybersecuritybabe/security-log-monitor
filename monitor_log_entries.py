"""Monitor log files for warning and error messages."""
import argparse # command-line argument parsing
import re # regular expressions for pattern matching
import time # time-related functions
from pathlib import Path # pathlib for filesystem paths

ALERT_PATTERN = re.compile(
    r"\b(?:ERROR|WARNING)\b",
    re.IGNORECASE
)

def analyze_line(line):
    return bool(ALERT_PATTERN.search(line))

# Continuously read new log lines and surface entries that indicate potential issues.
def monitor_logs(log_file, live=False):
    """Analyze existing log entries or monitor for new ones."""

    log_path = Path(log_file)

    if not log_path.is_file():
        raise FileNotFoundError(
            f"Log file '{log_path}' does not exist."
        )

    alert_count = 0

    try:
        with log_path.open(
            "r", encoding="utf-8"
        ) as file:

            if live:
                # Ignore existing lines and only monitor for new entries.
                file.seek(0, 2)
                print(
                    f"Monitoring '{log_path}' for new log entries. "
                    "(Ctrl+C to stop.)",
                    flush=True
                )

            while True:
                line = file.readline()

                if not line:
                    if not live:
                        break  # Exit if not in live monitoring mode.

                    time.sleep(0.5)  # Wait for new log entries to be written.
                    continue

                if analyze_line(line):
                    alert_count += 1
                    print(
                        f"ALERT: {line.strip()}",
                        flush=True
                    )

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Exiting...")

    print(
        f"Total alerts found: {alert_count}"
    )

    return alert_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Analyze existing security logs "
            "or monitor new log entries for potential issues."
        )
    )

    parser.add_argument(
        "log_file",
        help="Path to the log file to analyze"
    )

    parser.add_argument(
        "--live",
        action="store_true",
        help="Monitor the log file for new entries in real-time"
    )

    args = parser.parse_args()

    monitor_logs(
        log_file=args.log_file,
        live=args.live
    )