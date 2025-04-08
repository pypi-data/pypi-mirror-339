import subprocess
from pathlib import Path

def test_cli_report(tmp_path, monkeypatch, capsys):
    # Simulate a project directory name
    monkeypatch.setattr("pathlib.Path.cwd", lambda: tmp_path / "fake_project")

    # Compute where the logger will write logs
    log_dir = Path.home() / ".slowpoke" / "fake_project" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "slowpoke.log"

    # Write a dummy log entry
    log_path.write_text('{"method": "GET", "route": "/", "status_code": 200, "duration_ms": 150}\n')

    from slowpoke.cli import report
    report()

    out = capsys.readouterr().out
    assert "GET" in out
    assert "/" in out
    assert "200" in out
