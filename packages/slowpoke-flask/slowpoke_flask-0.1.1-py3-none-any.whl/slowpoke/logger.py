import time
from flask import request
import json
import os
from pathlib import Path
from datetime import datetime
import hashlib

def get_project_log_file():
    cwd = Path.cwd()
    project_hash = hashlib.md5(str(cwd).encode()).hexdigest()[:8]  # short hash for uniqueness
    project_name = cwd.name or "default"
    safe_project_name = project_name.replace(" ", "_").replace(".", "_")
    
    log_dir = Path.home() / '.slowpoke' / 'logs' / f"{safe_project_name}_{project_hash}"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    return log_dir / 'slowpoke.log'

LOG_FILE = get_project_log_file()

def log_slow_request(request, response, duration):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "route": request.path,
        "status_code": response.status_code,
        "duration_ms": round(duration, 2)
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
