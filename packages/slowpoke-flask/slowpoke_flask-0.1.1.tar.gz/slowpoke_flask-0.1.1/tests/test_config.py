from unittest.mock import patch
from slowpoke.config import get_config

def test_default_config():
    # Simulate config file not existing
    with patch("pathlib.Path.exists", return_value=False):
        config = get_config()
        assert config["threshold_ms"] == 100
