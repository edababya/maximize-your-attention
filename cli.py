"""Command-line interface for Maximize Your Attention."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


COMMANDS = (
    "ingest",
    "briefing",
    "ask",
    "rank",
    "log-prediction",
    "report",
)


def not_implemented(_: argparse.Namespace) -> None:
    """Handle Phase 1 command placeholders."""

    print("not implemented yet")


def build_parser() -> argparse.ArgumentParser:
    """Build the stable Phase 1 command-line surface."""

    parser = argparse.ArgumentParser(
        description="Personal cognition and attention harness for investors."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in COMMANDS:
        subparser = subparsers.add_parser(command)
        subparser.set_defaults(handler=not_implemented)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and run the selected command."""

    args = build_parser().parse_args(argv)
    args.handler(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
