"""Banco de preguntas de astrofísica, en su forma cruda del JSON."""

import json
from pathlib import Path
from typing import Any

__all__ = ["astrofisica"]

_FILE = Path(__file__).with_name("astrofisica.json")

astrofisica: list[dict[str, Any]] = json.loads(_FILE.read_text(encoding="utf-8"))
