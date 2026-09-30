"""Environment-backed application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Config:
    """Runtime settings loaded from environment variables."""

    ai_api_key: str
    ai_api_base: str
    ai_model: str
    embed_model: str
    db_path: Path


def load() -> Config:
    """Load configuration without reading files or making network calls."""

    return Config(
        ai_api_key=os.getenv("AI_API_KEY", ""),
        ai_api_base=os.getenv("AI_API_BASE", "https://api.deepseek.com"),
        ai_model=os.getenv("AI_MODEL", "deepseek-chat"),
        embed_model=os.getenv(
            "EMBED_MODEL", "Alibaba-NLP/gte-modernbert-base"
        ),
        db_path=Path(os.getenv("DB_PATH", "attention.db")),
    )
