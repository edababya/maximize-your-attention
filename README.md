# Maximize Your Attention

Maximize Your Attention is a personal cognition and attention harness for a professional investor working across AI infrastructure, foundation models, robotics, and semiconductors. Its long-term purpose is to connect projects, people, events, signals, investment theses, and predictions so that daily attention follows the most consequential evidence rather than the noisiest information.

## Problem

Investment judgment is distributed across notes, news, meetings, people, theses, and forecasts. Without a durable structure, important links are easy to lose, external milestones are easy to miss, and past predictions are difficult to calibrate. This project creates a local, inspectable foundation for that workflow.

## Phase 1 scope

Phase 1 provides only the scaffold and data model:

- A SQLite schema for projects, people, events, signals, theses, predictions, and typed edges.
- Full-text search over signal titles and summaries, synchronized by database triggers.
- Typed Python dataclasses plus reusable ID and timestamp helpers.
- Environment-based configuration.
- An `argparse` CLI surface for future workflows.
- Placeholder directories for ingestion, graph, cognition, and prediction-ledger code.

Phase 1 does **not** implement feed ingestion, embeddings, model calls, graph linking, ranking, briefings, reports, or automation. The application makes no network calls.

## Architecture overview

```text
config.py          Environment-backed settings
models.py          Typed domain records and shared helpers
schema.sql         SQLite tables, constraints, indexes, and FTS5 triggers
cli.py             Stable command-line surface with Phase 1 stubs
ingest/            Future source-ingestion code
graph/             Future entity-linking code
brain/             Future reasoning and ranking code
ledger/            Future prediction-calibration code
inbox/             Future local intake area (archives are ignored)
briefings/         Future generated briefings
tests/             Focused schema and FTS synchronization smoke test
```

SQLite is the Phase 1 system of record. `signal_fts` is an external-content FTS5 table backed by `signal`; insert, update, and delete triggers keep the search index synchronized.

## Quickstart

Requires Python 3.11+ with SQLite FTS5 support.

```bash
cp .env.example .env
python -c "import config; print(config.load().db_path)"
python cli.py --help
python -m unittest discover -s tests -v
```

The Phase 1 code uses only the Python standard library. Packages in `requirements.txt` are reserved for future phases and are not needed for the checks above.

To initialize a local database:

```bash
python - <<'PY'
import sqlite3
from config import load

connection = sqlite3.connect(load().db_path)
connection.executescript(open("schema.sql", encoding="utf-8").read())
connection.close()
PY
```

All credentials must be supplied through environment variables. Never commit `.env` or API keys.
