"""Focused smoke checks for the SQLite schema and signal FTS triggers."""

from __future__ import annotations

import sqlite3
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "schema.sql").read_text(encoding="utf-8")


class SchemaSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.executescript(SCHEMA)

    def tearDown(self) -> None:
        self.connection.close()

    def fts_count(self, query: str) -> int:
        row = self.connection.execute(
            "SELECT count(*) FROM signal_fts WHERE signal_fts MATCH ?", (query,)
        ).fetchone()
        assert row is not None
        return int(row[0])

    def test_signal_fts_stays_synchronized(self) -> None:
        self.connection.execute(
            """
            INSERT INTO signal (
                id, source, kind, title, url, published_at, summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "0123456789ab",
                "smoke-test",
                "news",
                "Photon interconnect milestone",
                "https://example.com/signal",
                "2026-09-29T12:00:00Z",
                "A fabrication result for AI infrastructure.",
            ),
        )
        self.assertEqual(self.fts_count("photon"), 1)

        self.connection.execute(
            "UPDATE signal SET title = ?, summary = ? WHERE id = ?",
            (
                "Robotics deployment milestone",
                "A field result for embodied systems.",
                "0123456789ab",
            ),
        )
        self.assertEqual(self.fts_count("photon"), 0)
        self.assertEqual(self.fts_count("robotics"), 1)

        self.connection.execute(
            "DELETE FROM signal WHERE id = ?", ("0123456789ab",)
        )
        self.assertEqual(self.fts_count("robotics"), 0)


if __name__ == "__main__":
    unittest.main()
