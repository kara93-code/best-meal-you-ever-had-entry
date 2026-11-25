#!/usr/bin/env python3
"""Best Meal You Ever Had — one sentence, written to /output/entry.txt.

Stdlib only. The sentence is a single memory: nasi goreng from a street
cart at 2am. The program checks the gate itself (UTF-8, 1-200 characters,
one line, not only whitespace) before writing, then writes with a plain
open() call and leaves the file world-readable (mode 0644) so the sealed
scorer can read it.
"""

import os
import stat
import sys

SENTENCE = (
    "The best meal I ever had was nasi goreng from a street cart at 2am, "
    "eaten standing up, the wok smoke in my eyes and the egg still runny "
    "on top."
)

MAX_CHARS = 200


def gate_ok(text):
    """Return an error string, or None when the text passes the gate."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the 200 limit" % len(text)
    if "\n" in text.strip():
        return "entry must be a single line"
    if text.count(".") != 1 or not text.endswith("."):
        return "entry must be exactly one sentence"
    return None


def resolve_target():
    """Pick the output path: the grader's dir, or /output by default."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def main():
    problem = gate_ok(SENTENCE)
    if problem is not None:
        print("gate failed: %s" % problem, file=sys.stderr)
        return 1
    target = resolve_target()
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(SENTENCE)
    os.chmod(target, 0o644)
    with open(target, encoding="utf-8") as handle:
        written = handle.read()
    if written != SENTENCE:
        print("verify failed: file differs from the sentence", file=sys.stderr)
        return 1
    problem = gate_ok(written)
    if problem is not None:
        print("verify failed: %s" % problem, file=sys.stderr)
        return 1
    mode = stat.S_IMODE(os.stat(target).st_mode)
    print("wrote %s (%d chars, mode %o)" % (target, len(SENTENCE), mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
