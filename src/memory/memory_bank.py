# src/memory/memory_bank.py
"""
MemoryBank - persistent memory for ThreatGuard

Features:
- Loads memory from disk if present
- Auto-creates data directory and memory file
- Thread-safe in-memory store with atomic JSON writes
- Provides legacy-compatible API:
    - save(data)
    - store(data)
    - save_threat(payload)
    - save_hardening(payload)
    - export_memory() -> dict
    - get_all() -> list
"""

import json
import os
import threading
import time
import tempfile

DATA_DIR = os.path.join(os.getcwd(), "data")
MEMORY_FILE = os.path.join(DATA_DIR, "memory_bank.json")


class MemoryBank:
    def __init__(self, logger=None, file_path: str = None):
        self.logger = logger
        self._lock = threading.Lock()
        self._storage = {
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "threats": [],
            "hardening": [],
            "events": [],
        }

        # allow override for tests / custom path
        self.file_path = file_path or MEMORY_FILE

        # ensure data directory exists
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        except Exception:
            # best-effort; not fatal
            pass

        # try to load existing memory
        self._load_from_disk()

        if self.logger:
            self.logger.log(f"[MemoryBank] Initialized. file={self.file_path}")

    # Internal: atomic write
    def _atomic_write(self, path: str, data: str):
        dirn = os.path.dirname(path) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dirn, prefix=".memtmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)  # atomic on POSIX
        except Exception:
            # cleanup on failure
            try:
                os.remove(tmp_path)
            except Exception:
                pass
            raise

    def _load_from_disk(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # merge safe: keep expected keys
                    if isinstance(data, dict):
                        for k in ("threats", "hardening", "events"):
                            if k in data and isinstance(data[k], list):
                                self._storage[k] = data[k]
                        # copy other keys too if desired
                        for k, v in data.items():
                            if k not in self._storage:
                                self._storage[k] = v
                        if self.logger:
                            self.logger.log(f"[MemoryBank] Loaded memory from {self.file_path}")
        except Exception as e:
            if self.logger:
                self.logger.log(f"[MemoryBank] Failed to load memory: {e}")

    def _flush_to_disk(self):
        with self._lock:
            try:
                raw = json.dumps(self._storage, indent=2, ensure_ascii=False)
                self._atomic_write(self.file_path, raw)
                if self.logger:
                    self.logger.log(f"[MemoryBank] Flushed memory to disk ({self.file_path})")
            except Exception as e:
                if self.logger:
                    self.logger.log(f"[MemoryBank] Error writing memory to disk: {e}")

    # Generic save: append to "events"
    def save(self, data):
        with self._lock:
            self._storage.setdefault("events", []).append(
                {"ts": time.time(), "payload": data}
            )
        # write out async-safe immediate flush
        self._flush_to_disk()
        return True

    # store is alias for save (some code used memory.store)
    def store(self, data):
        return self.save(data)

    # specific helper for threats
    def save_threat(self, payload: dict):
        with self._lock:
            self._storage.setdefault("threats", []).append(
                {"ts": time.time(), "threat": payload}
            )
        self._flush_to_disk()
        return True

    # specific helper for hardening records
    def save_hardening(self, payload: dict):
        with self._lock:
            self._storage.setdefault("hardening", []).append(
                {"ts": time.time(), "hardening": payload}
            )
        self._flush_to_disk()
        return True

    # Export full snapshot (safe copy)
    def export_memory(self):
        with self._lock:
            return json.loads(json.dumps(self._storage))

    # get all events/threats
    def get_all(self):
        with self._lock:
            return json.loads(json.dumps(self._storage))

    # convenience: direct access to threats list (read-only copy)
    def get_threats(self):
        with self._lock:
            return json.loads(json.dumps(self._storage.get("threats", [])))
