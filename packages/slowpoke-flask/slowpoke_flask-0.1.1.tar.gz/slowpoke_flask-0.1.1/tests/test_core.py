import time
from flask import Flask
from pathlib import Path
import json

from slowpoke.core import monitor

def test_monitor_logs_slow_request(tmp_path, monkeypatch):
    # Simulate project directory name
    monkeypatch.setattr("pathlib.Path.cwd", lambda: tmp_path / "fake_project")

    app = Flask(__name__)
    monitor(app)

    @app.route("/slow")
    def slow():
        time.sleep(0.15)  # 150ms > 100ms default threshold
        return "slow response"

    with app.test_client() as client:
        client.get("/slow")

    # Get the actual log file path
    log_file = Path.home() / ".slowpoke" / "fake_project" / "logs" / "slowpoke.log"
    assert log_file.exists()

    logs = log_file.read_text().strip().split("\n")
    assert len(logs) >= 1
    for log in logs:
        entry = json.loads(log)
        if entry["route"] == "/slow":
            assert entry["method"] == "GET"
            assert entry["status_code"] == 200
            assert entry["duration_ms"] > 100
            break
    else:
        raise AssertionError("No log entry found for /slow route")

