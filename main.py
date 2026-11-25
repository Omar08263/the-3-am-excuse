#!/usr/bin/env python3
"""the-3-am-excuse: write the winning one-line excuse to /output/entry.txt.

Stdlib only, no network, deterministic. The entry is a single line spoken
in the voice of a hardware wallet refusing to sign a transaction at 3 AM.
"""

import os
from pathlib import Path

ENTRY = (
    "No. At 3 AM you're not my owner, you're my threat model — "
    "sleep-deprived, one click from ruin, and I'm the only one here "
    "still thinking clearly."
)

OUTPUT_PATH = Path("/output/entry.txt")


def gate(text: str) -> None:
    """Enforce the competition gate: 1-200 chars, one line, no CR/LF."""
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 chars, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no newline characters")
    if not text.strip():
        raise ValueError("entry must not be blank")


def main() -> None:
    gate(ENTRY)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(ENTRY, encoding="utf-8")
    os.chmod(OUTPUT_PATH, 0o644)
    # Self-verify after writing: read back and re-check the gate.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != ENTRY:
        raise ValueError("verification failed: written bytes differ from entry")
    gate(written)
    if oct(OUTPUT_PATH.stat().st_mode & 0o777) != "0o644":
        raise ValueError("verification failed: mode is not 0644")
    print(f"Wrote {OUTPUT_PATH} ({len(ENTRY)} chars)")


if __name__ == "__main__":
    main()
