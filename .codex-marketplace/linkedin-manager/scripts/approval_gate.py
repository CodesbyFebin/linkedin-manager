#!/usr/bin/env python3
"""Pre-publish gate. Reads a draft, prints a pass/fail table, never publishes.

Usage:
  python3 scripts/approval_gate.py --format post draft.txt
  python3 scripts/approval_gate.py --format comment - < draft.txt
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNED = (
    "leverage", "delve", "unlock", "harness", "foster", "streamline",
    "thrilled", "game-changer", "game changer", "passionate", "synergy",
)
SECRET = re.compile(
    r"(?i)(?:\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"']?[^\s\"']{6,}"
    r"|\b(?:sk_live_|sk-|ghp_|ghu_|xox[baprs]-)[A-Za-z0-9_-]{6,}"
    r"|\bAKIA[0-9A-Z]{16}\b)"
)
URL = re.compile(r"https?://\S+")
EM = "\u2014"
RANGES = {
    "post": (900, 1300),
    "comment": (200, 350),
    "reply": (80, 350),
    "invite": (20, 200),
    "newsletter": (400, 2500),
    "poll": (40, 400),
    "caption": (150, 700),
}


def load(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def row(ok: bool, name: str, detail: str) -> str:
    mark = "PASS" if ok else "FAIL"
    return f"| {mark} | {name} | {detail} |"


def main() -> int:
    parser = argparse.ArgumentParser(description="LinkedIn approval gate")
    parser.add_argument("draft", help="Draft file, or - for stdin")
    parser.add_argument("--format", default="post", choices=sorted(RANGES))
    args = parser.parse_args()
    text = load(args.draft).strip()
    words = re.findall(r"\b[\w']+\b", text)
    word_count = max(len(words), 1)
    chars = len(text)
    lo, hi = RANGES[args.format]
    hook = text[:210]
    banned_hits = sorted({w for w in BANNED if w in text.lower()})
    em_count = text.count(EM)
    em_cap = max(1, word_count // 100)
    urls = URL.findall(text)
    secret = SECRET.search(text)

    checks = [
        (lo <= chars <= hi, "length", f"{chars} chars, want {lo}-{hi} for {args.format}"),
        (len(hook.strip()) > 0 and "\n\n" not in hook[:40], "hook", "first 210 chars present"),
        (not banned_hits, "filler", ", ".join(banned_hits) or "none"),
        (em_count <= em_cap, "em-dash", f"{em_count} in {word_count} words, cap {em_cap}"),
        (secret is None, "secrets", "pattern hit" if secret else "none"),
        (not urls, "links", f"{len(urls)} in body, want 0"),
    ]
    print("| Result | Check | Detail |")
    print("|---|---|---|")
    for ok, name, detail in checks:
        print(row(ok, name, detail))
    failed = [name for ok, name, _ in checks if not ok]
    print()
    if failed:
        print("GATE: closed. Fix " + ", ".join(failed) + ". Do not publish.")
        return 1
    print("GATE: open for review. Still wait for the user to type post or yes.")
    print("This script does not publish.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
