import json
from pathlib import Path
from slowpoke.logger import log_slow_request

def test_log_slow_request(tmp_path, monkeypatch):
    # Monkeypatch Path.cwd() to simulate a project directory
    monkeypatch.setattr("pathlib.Path.cwd", lambda: tmp_path / "my_test_project")

    # Simulate a request and response
    class DummyRequest:
        method = "GET"
        path = "/test-route"

    class DummyResponse:
        status_code = 200

    # Call the logger
    log_slow_request(DummyRequest(), DummyResponse(), 123.45)

    # Check the log file
    log_file = Path.home() / ".slowpoke" / "my_test_project" / "logs" / "slowpoke.log"

    assert log_file.exists()

    with open(log_file) as f:
        lines = f.readlines()
        assert len(lines) == 1
        log_entry = json.loads(lines[0])
        assert log_entry["method"] == "GET"
        assert log_entry["route"] == "/test-route"
        assert log_entry["status_code"] == 200
        assert log_entry["duration_ms"] == 123.45
