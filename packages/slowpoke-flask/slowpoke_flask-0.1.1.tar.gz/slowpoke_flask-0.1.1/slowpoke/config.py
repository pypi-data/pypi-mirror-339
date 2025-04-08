import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".slowpoke" / "config.json"

DEFAULT_CONFIG = {
    "threshold_ms": 100
}

def get_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG
