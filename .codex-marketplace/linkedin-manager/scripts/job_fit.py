#!/usr/bin/env python3
"""Score a pasted job description against a local profile. No network.

Usage:
  python3 scripts/job_fit.py job.txt profile.txt
profile.txt is optional plain text (role, skills, cities). Missing profile
prints the extracted fields only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TITLE = re.compile(r"(?im)^(?:title|role)\s*[:\-]\s*(.+)$")
LOC = re.compile(r"(?im)^(?:location|city)\s*[:\-]\s*(.+)$")
REMOTE = re.compile(r"(?i)\b(remote|hybrid|on-?site)\b")


def fields(text: str) -> dict:
    title = TITLE.search(text)
    loc = LOC.search(text)
    return {
        "title": title.group(1).strip() if title else "",
        "location": loc.group(1).strip() if loc else "",
        "mode": ", ".join(sorted(set(m.group(1).lower() for m in REMOTE.finditer(text)))) or "unstated",
        "chars": len(text.strip()),
    }


def tokens(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9+.#]{2,}", text)}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: job_fit.py job.txt [profile.txt]", file=sys.stderr)
        return 2
    job = Path(sys.argv[1]).read_text(encoding="utf-8")
    info = fields(job)
    print("| Field | Value |")
    print("|---|---|")
    for k, v in info.items():
        print(f"| {k} | {v or 'missing'} |")
    if len(sys.argv) < 3:
        print("\nNo profile file. Fit not scored. Paste a profile to compare.")
        print("Do not apply from this script.")
        return 0
    profile = Path(sys.argv[2]).read_text(encoding="utf-8")
    overlap = tokens(job) & tokens(profile)
    useful = sorted(w for w in overlap if w not in {"the", "and", "for", "with", "you"})[:12]
    print("\nOverlap terms: " + (", ".join(useful) or "none"))
    print("This is a term overlap, not a hire decision. Do not apply from this script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
