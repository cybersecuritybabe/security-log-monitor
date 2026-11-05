import pytest

from monitor_log_entries import analyze_line, monitor_logs

@pytest.mark.parametrize(
    "log_entry, expected",
    [
        ("2024-06-01 12:00:00 INFO Starting process", False),
        ("2024-06-01 12:01:00 WARNING Disk space low", True),
        ("2024-06-01 12:02:00 ERROR Failed to connect to database", True),
        ("2024-06-01 12:03:00 DEBUG Connection established", False),
        ("2024-06-01 12:04:00 error Unexpected shutdown", True),
        ("2024-06-01 12:05:00 warning High memory usage", True),
        ("2024-06-01 12:06:00 INFO Process completed successfully", False),
        ("2024-06-01 12:07:00 INFO ERRORLESS operation", False),
        ("2024-06-01 12:08:00 INFO PREWARNING condition", False),
        ("2024-06-01 12:09:00 WARNING: Disk usage exceeded threshold", True),
        ("2024-06-01 12:10:00 ERROR: Database connection timeout", True),
    ]
)

def test_regex_boundaries(log_entry, expected):
    """Verify whole-word keyword matching."""

    assert analyze_line(log_entry) is expected

def test_monitor_logs_existing_entries(tmp_path, capsys):
    log_file = tmp_path / "test_log.log"

    log_file.write_text(
        "2024-06-01 12:00:00 INFO Starting process\n"
        "2024-06-01 12:01:00 WARNING Disk space low\n"
        "2024-06-01 12:02:00 ERROR Failed to connect to database\n"
        "2024-06-01 12:03:00 DEBUG Connection established\n"
    )

    count = monitor_logs(
        log_file,
        live=False
    )

    output = capsys.readouterr()
    assert "ALERT: 2024-06-01 12:01:00 WARNING Disk space low" in output.out
    assert "ALERT: 2024-06-01 12:02:00 ERROR Failed to connect to database" in output.out

def test_monitor_logs_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        monitor_logs("nonexistent.log", live=False)

def test_monitor_logs_empty_file(tmp_path, capsys):
    """An empty file should produce zero alerts."""

    log_file = tmp_path / "empty.log"

    log_file.write_text(
        "",
        encoding="utf-8"
    )

    count = monitor_logs(
        log_file,
        live=False
    )

    output = capsys.readouterr().out

    assert count == 0
    assert "Total alerts found: 0" in output
    assert "ALERT:" not in output