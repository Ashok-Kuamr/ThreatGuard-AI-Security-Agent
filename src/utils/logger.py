# logger.py
"""
Simple Logger Utility for ThreatGuard.
Adds timestamps, message formatting, and optional in-memory storage.
"""

import datetime


class ThreatLogger:
    def __init__(self, store_in_memory: bool = True):
        self.store_in_memory = store_in_memory
        self.logs = [] if store_in_memory else None

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"

        print(line)

        if self.store_in_memory and self.logs is not None:
            self.logs.append(line)

    def get_logs(self):
        return self.logs if self.store_in_memory else []
