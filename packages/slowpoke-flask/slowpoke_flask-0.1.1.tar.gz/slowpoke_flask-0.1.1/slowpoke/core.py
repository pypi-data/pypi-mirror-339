import time
from flask import request
from flask import g
from .logger import log_slow_request
from .config import get_config

"""
the heart of the slowpoke package
"""

def monitor(app):
    
    config = get_config()
    threshold_ms = config.get("threshold_ms", 100)

    @app.before_request
    def _before_request():
        request._slowpoke_start= time.time()
        
        
    @app.after_request
    def _after_request(response):
        start = getattr(request, '_slowpoke_start', None)
        
        if start:
            duration = (time.time() - start) * 1000
            if duration > threshold_ms:
                print(f"[Debug] {request.method} {request.path} took {duration:.2f}ms - slow")
                log_slow_request(request, response, duration)
                
        return response