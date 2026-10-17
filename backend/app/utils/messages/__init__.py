"""Textos de mensajes del proyecto, en su forma cruda del JSON."""

import json
from pathlib import Path

__all__ = ["info"]

_FILE = Path(__file__).with_name("info.json")

info: dict[str, str] = json.loads(_FILE.read_text(encoding="utf-8"))
