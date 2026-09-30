"""Typed domain records for the Phase 1 data model."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timezone


def new_id() -> str:
    """Return a random 12-character hexadecimal identifier."""

    return secrets.token_hex(6)


def utc_now_iso() -> str:
    """Return the current UTC timestamp as ISO-8601 text."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


@dataclass(slots=True)
class Project:
    id: str
    name: str
    sector: str | None
    stage: str | None
    status: str
    thesis_tags: str | None
    notes: str | None
    created_at: str
    updated_at: str


@dataclass(slots=True)
class Person:
    id: str
    name: str
    role: str | None
    org: str | None
    x_handle: str | None
    notes: str | None
    last_contact: str | None


@dataclass(slots=True)
class Event:
    id: str
    title: str
    kind: str
    starts_at: str | None
    location: str | None
    notes: str | None
    status: str | None


@dataclass(slots=True)
class Signal:
    id: str
    source: str
    kind: str
    title: str
    url: str | None
    published_at: str | None
    summary: str | None
    importance: int = 0
    embedding: bytes | None = None


@dataclass(slots=True)
class Thesis:
    id: str
    title: str
    statement: str
    confidence: float
    status: str
    created_at: str


@dataclass(slots=True)
class Prediction:
    id: str
    statement: str
    confidence: float
    thesis_id: str | None
    created_at: str
    resolve_by: str | None
    outcome: str = "pending"


@dataclass(slots=True)
class Edge:
    id: int | None
    from_type: str
    from_id: str
    to_type: str
    to_id: str
    relation: str
    weight: float = 1.0
