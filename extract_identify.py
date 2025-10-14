#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract species identifiers from a .tre file (Newick-like) and write one per line.

Example identifier format:
    B2CBB8_Poa_nemoralis_Poaceae

We assume patterns like:
  - First chunk: alnum+ (e.g., accession/hash-like)
  - Followed by >=2 underscore-separated taxon-like chunks (letters and optional dashes)

This script:
  - reads the tree file as text (tolerant to encoding glitches),
  - uses a robust regex to find identifiers among punctuation,
  - writes them line-by-line to the output file,
  - prints the total count (and unique count if requested) to stderr.

Usage:
  ./extract_identifiers.py pgi.tre identifiers.txt
  ./extract_identifiers.py pgi.tre identifiers.txt --unique
"""

import re
import sys
import argparse
from pathlib import Path

# Regex notes:
#   \b alone can fail around punctuation in Newick; use lookarounds to be more permissive.
#   First chunk: [A-Za-z0-9]+
#   Next chunks: (_ + letter + letters/dashes) repeated at least twice → {2,}
IDENT_RE = re.compile(
    r"""(?<!\S)               # left boundary: start or whitespace-like
        ([A-Za-z0-9]+         # first chunk (captured)
         (?:_[A-Za-z][A-Za-z-]*){2,})  # ≥2 underscore chunks
        (?!\S)                # right boundary: end or whitespace-like
    """,
    re.VERBOSE,
)

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Extract species identifiers from a tree file."
    )
    ap.add_argument("tree_file", help=".tre file (Newick-like text)")
    ap.add_argument("out_txt", help="Output text file, one identifier per line")
    ap.add_argument("--unique", action="store_true",
                    help="Write unique identifiers only (preserve first-seen order)")
    return ap.parse_args()

def main():
    args = parse_args()
    in_path = Path(args.tree_file)
    out_path = Path(args.out_txt)

    if not in_path.exists():
        print(f"❌ Input not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    # Read with tolerant error handling (tree files can contain odd bytes)
    text = in_path.read_text(encoding="utf-8", errors="replace")

    # Find all identifiers (captured group 1)
    idents = [m.group(1) for m in IDENT_RE.finditer(text)]

    if args.unique:
        # Ordered de-dup (preserve first occurrence)
        seen = set()
        uniq = []
        for x in idents:
            if x not in seen:
                seen.add(x)
                uniq.append(x)
        idents_to_write = uniq
    else:
        idents_to_write = idents

    # Write output
    try:
        with open(out_path, "w", encoding="utf-8", newline="") as out:
            for ident in idents_to_write:
                out.write(ident + "\n")
    except OSError as e:
        print(f"❌ Failed to write output: {e}", file=sys.stderr)
        sys.exit(1)

    # Report counts to stderr (so stdout remains clean if piped)
    total = len(idents)
    written = len(idents_to_write)
    if args.unique:
        print(f"✅ Total matches: {total}; unique written: {written} → {out_path.resolve()}",
              file=sys.stderr)
    else:
        print(f"✅ Total matches written: {written} → {out_path.resolve()}",
              file=sys.stderr)

if __name__ == "__main__":
    main()
