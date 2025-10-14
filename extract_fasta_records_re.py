#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract FASTA records containing a given subsequence pattern (regex-based).

Usage:
    ./extract_fasta_records_re.py regions.fna ATCTCTC interesting_sequences.fna

You can also provide regular expressions:
    ./extract_fasta_records_re.py regions.fna "ATC[AT]CTC" hits.fna

By default, matching is case-insensitive.
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


def read_fasta(path: Path) -> List[Tuple[str, str]]:
    """Return list of (header, sequence)."""
    records = []
    header = None
    parts=[]
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(parts)))
                header = line[1:].strip()
                parts = []
            else:
                parts.append(line)
        if header is not None:
            records.append((header, "".join(parts)))
    return records


def write_fasta(path，records):
    """Write selected records to new FASTA."""
    with open(path, "w", encoding="utf-8", newline="") as out:
        for h, s in records:
            out.write(f">{h}\n{s}\n")


def main():
    if len(sys.argv) != 4:
        print("Usage: ./extract_fasta_records_re.py <input.fna> <pattern> <output.fna>", file=sys.stderr)
        sys.exit(1)

    in_path = Path(sys.argv[1])
    pattern = sys.argv[2]
    out_path = Path(sys.argv[3])

    if not in_path.exists():
        print(f"❌ Input FASTA not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    # Compile regex for efficiency
    regex = re.compile(pattern, re.IGNORECASE)  # 不区分大小写
    records = read_fasta(in_path)

    hits = [(h, s) for (h, s) in records if regex.search(s)]
    write_fasta(out_path, hits)

    print(f"✅ {len(hits)} / {len(records)} records written → {out_path.resolve()}")


if __name__ == "__main__":
    main()
