import os
from pathlib import Path
from typing import Any, Dict
import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "default_config.yaml"

def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    target_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {target_path}")
    with open(target_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
