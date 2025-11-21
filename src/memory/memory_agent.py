# memory_agent.py
"""
Simple MemoryAgent for long-term storage of threat logs.
In production, this could be replaced with Firestore, Redis, Mongo, or SQL.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any


class MemoryAgent:
    def __init__(self, storage_path="memory_store.json", logger=None):
        self.storage_path = storage_path
        self.logger = logger

        # Create file if missing
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as f:
                json.dump({"threat_logs": []}, f)

    def store(self, threat_entry: Dict[str, Any]) -> None:
        """Store a threat entry with timestamp."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "threat": threat_entry
        }

        with open(self.storage_path, "r") as f:
            data = json.load(f)

        data["threat_logs"].append(entry)

        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2)

        if self.logger:
            self.logger.log(f"[MemoryAgent] Stored new threat: {entry}")

    def load_all(self):
        """Return all stored threat entries."""
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def search(self, key: str, value: str):
        """Search stored logs."""
        logs = self.load_all()["threat_logs"]
        return [log for log in logs if log["threat"].get(key) == value]
