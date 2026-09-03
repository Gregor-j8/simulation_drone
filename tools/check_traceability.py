#!/usr/bin/env python3
"""Fail CI if any requirement lacks a traceability entry, or vice versa.

M0: checks structural consistency between docs/requirements.md and
docs/traceability.csv. From M6 it will also assert the linked test passed
(by parsing the ctest / pytest result files).
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_MD = ROOT / "docs" / "requirements.md"
TRACE_CSV = ROOT / "docs" / "traceability.csv"

REQ_ID = re.compile(r"^\| (?P<id>[A-Z]{2,4}-\d{3}) \|")


def requirement_ids() -> set[str]:
    ids: set[str] = set()
    for line in REQ_MD.read_text(encoding="utf-8").splitlines():
        m = REQ_ID.match(line)
        if m:
            ids.add(m.group("id"))
    return ids


def traced_ids() -> set[str]:
    with TRACE_CSV.open(encoding="utf-8", newline="") as fh:
        return {row["req_id"] for row in csv.DictReader(fh)}


def main() -> int:
    reqs = requirement_ids()
    traced = traced_ids()

    untraced = sorted(reqs - traced)
    orphaned = sorted(traced - reqs)

    for rid in untraced:
        print(f"ERROR: {rid} has no traceability entry", file=sys.stderr)
    for rid in orphaned:
        print(f"ERROR: traceability references unknown requirement {rid}", file=sys.stderr)

    if untraced or orphaned:
        return 1
    print(f"traceability OK: {len(reqs)} requirements, all linked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
