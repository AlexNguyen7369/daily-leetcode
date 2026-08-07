"""User-editable settings, stored in config.json at the project root."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config.json")

DEFAULTS: Dict[str, Any] = {
    "auto_push": True,
    "remote": "https://github.com/AlexNguyen7369/daily-leetcode.git",
    "branch": "main",
    "commit_prefix": "solve",
    "difficulty_mix": "both",   # both | easy | medium
    "server_port": 8777,
    "seed": None,               # None -> generated once and stored
}


def load() -> Dict[str, Any]:
    values = dict(DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
                values.update(json.load(handle))
        except (json.JSONDecodeError, OSError):
            pass
    return values


def save(values: Dict[str, Any]) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as handle:
        json.dump(values, handle, indent=2)
        handle.write("\n")


def get(key: str) -> Any:
    return load().get(key, DEFAULTS.get(key))


def set_value(key: str, value: Any) -> Dict[str, Any]:
    values = load()
    values[key] = value
    save(values)
    return values
