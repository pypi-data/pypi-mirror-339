import sys
from .logger import LOG_FILE  # Make sure logger.py exists and has LOG_FILE

def report():
    try:
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
            if not logs:
                print("No slow requests logged yet.")
            for line in logs:
                print(line.strip())
    except FileNotFoundError:
        print("Log file not found.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        report()
    else:
        print("Usage: slowpoke report")
