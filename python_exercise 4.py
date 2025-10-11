reated on Thu Oct  9 09:56:25 2025

@author: yukim
"""

"""
Date: 2025-10-09
Author: Yiran Chen
Description:
  4. File handling — Spyder-style solutions with safe fallbacks.
  Topics: pathlib.Path, encoding, CSV I/O, FASTA parsing, GC%, line lookup, FASTQ→FASTA.

Usage:
  Run cell-by-cell with Ctrl+Enter (Spyder style).
  Cells that accept CLI args via sys.argv also include safe fallbacks.
  Shebang (if saving as a script):  #!/usr/bin/env python3
"""

#%% 4.1 Pathlib — a) import Path from pathlib
from pathlib import Path

#%% 4.1 Pathlib — b) print CWD & HOME and their types
cwd = Path.cwd() #working directory
home = Path.home()
print("CWD:", cwd, type(cwd))
print("HOME:", home, type(home))

#%% 4.1 Pathlib — c) make parent-of-cwd / "new_dir"
new_dir = cwd.parent.joinpath("new_dir")
new_dir.mkdir(parents=True, exist_ok=True)
print("Created or exists:", new_dir, "->", new_dir.exists())

#%% 4.1 Pathlib — d) list all HOME subdirs containing chosen letter
chosen = "a"  # change as you like
dirs_with_letter = [p for p in home.iterdir() if p.is_dir() and chosen in p.name]
print(f"Directories in HOME containing '{chosen}':")
for p in dirs_with_letter:
    print("  ", p)

#%% 4.1 Pathlib — e) match files by pattern; print stem and type
# Example: all *.txt directly under HOME
for p in home.glob("*.txt"):
    if p.is_file():
        print("Stem:", p.stem, "| is_file:", p.is_file())

#%% 4.1 Pathlib — f) Path from string; check exists
maybe_path = home / "possibly_missing_file.xyz"
print(f"{maybe_path} exists?", maybe_path.exists())

#%% 4.2 Encodings & CSV — a) ASCII encode a Swedish sentence
text = "är det du som har kaffebrödet, Gösta?"
print("Original:", text)
try:
    ascii_bytes = text.encode("ascii")
    print("ASCII bytes:", ascii_bytes)
except UnicodeEncodeError as e:
    print("ASCII encode failed:", e)
    print("Ignoring non-ASCII:", text.encode("ascii", errors="ignore"))
    print("Replacing non-ASCII:", text.encode("ascii", errors="replace"))

#%% 4.2 Encodings & CSV — b) write a tiny CSV (4x4) with a numeric column
csv_path = Path("demo_table.csv")
rows = [
    {"name":"alpha", "count":3, "score":1.5, "tag":"A"},
    {"name":"beta",  "count":7, "score":2.0, "tag":"B"},
    {"name":"gamma", "count":1, "score":9.2, "tag":"C"},
    {"name":"delta", "count":5, "score":3.3, "tag":"D"},
]
headers = ["name","count","score","tag"]
with open(csv_path, "w", encoding="utf-8") as fh:
    fh.write(",".join(headers) + "\n")
    for r in rows:
        fh.write(f"{r['name']},{r['count']},{r['score']},{r['tag']}\n")
print("Wrote CSV ->", csv_path.resolve())

#%% 4.2 Encodings & CSV — c) read CSV; compute mean/median/max/min of 'score'
scores = []
with open(csv_path, "r", encoding="utf-8") as fh:
    fh.readline()  # skip header
    for line in fh:
        if not line.strip(): continue
        name, count, score, tag = line.strip().split(",")
        scores.append(float(score))
scores.sort()
n = len(scores)
mean = sum(scores)/n
median = scores[n//2] if n%2==1 else 0.5*(scores[n//2-1] + scores[n//2])
print(f"score stats -> mean:{mean:.3f} median:{median:.3f} max:{max(scores):.3f} min:{min(scores):.3f}")

#%% 4.3 Get IDs from FASTA — with sys.argv 

# 定义文件路径
# parse_ids_from_fasta.py
from pathlib import Path
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_ids_from_fasta.py input.fa output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)

    ids = []

    # Extract IDs
    with open(input_file, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if line.startswith(">"):
                seq_id = line[1:].split()[0]
                ids.append(seq_id)

    # Write to output
    with open(output_file, "w", encoding="utf-8") as fout:
        for i in ids:
            fout.write(i + "\n")

    print(f"✅ Extracted {len(ids)} IDs → {Path(output_file).resolve()}")

if __name__ == "__main__":
    main()

#%% 4.4 Append GC% to FASTA headers — CLI style with fallback
#!/usr/bin/env python3
from pathlib import Path
import argparse

def gc_percent(seq: str) -> float:
    """
    GC% = (G + C) / length * 100, after removing whitespace and uppercasing.
    """
    s = ''.join(seq.split()).upper()
    if not s:
        return 0.0
    return (s.count('G') + s.count('C')) * 100.0 / len(s)

def append_gc_to_fasta(in_path: Path, out_path: Path) -> None:
    out_lines = []
    header = None
    parts = []

    with open(in_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith(">"):
                # flush previous sequence
                if header is not None:
                    seq = "".join(parts)
                    out_lines.append(f"{header} GC:{gc_percent(seq):.1f}%\n")
                    out_lines.append(seq + "\n")
                header = line.strip()
                parts = []
            else:
                parts.append(line.strip())

    # flush last sequence
    if header is not None:
        seq = "".join(parts)
        out_lines.append(f"{header} GC:{gc_percent(seq):.1f}%\n")
        out_lines.append(seq + "\n")

    with open(out_path, "w", encoding="utf-8") as fo:
        fo.writelines(out_lines)

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Append GC%% to FASTA headers."
    )
    ap.add_argument("input_fasta", help="Input FASTA file (e.g., paxillus.fna)")
    ap.add_argument("output_fasta", help="Output FASTA with GC%% in headers")
    return ap.parse_args()

def main():
    args = parse_args()
    in_path = Path(args.input_fasta)
    out_path = Path(args.output_fasta)

    if not in_path.exists():
        raise SystemExit(f"❌ Input file not found: {in_path}")

    append_gc_to_fasta(in_path, out_path)
    print(f"✅ Done. Wrote -> {out_path.resolve()}")

if __name__ == "__main__":
    main()
#%% 4.5 Find header line number by sequence ID — print line or error
# gc_append_fasta.py
import argparse
from pathlib import Path

def gc_percent(seq: str) -> float:
    s = seq.upper()
    gc = s.count("G") + s.count("C")
    n = len(s)
    return (gc / n * 100.0) if n else 0.0

def process(in_path: Path, out_path: Path) -> int:
    written = 0
    header = None
    seq_lines = []

    with in_path.open("r", encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            if line.startswith(">"):
                # flush previous record
                if header is not None:
                    seq = "".join(seq_lines).replace(" ", "")
                    pct = gc_percent(seq)
                    fout.write(f"{header} GC:{pct:.1f}%\n")
                    for sl in seq_lines:
                        fout.write(sl + "\n")
                    written += 1
                # start new record (keep header exactly as-is, minus trailing \n)
                header = line.rstrip("\n")
                seq_lines = []
            else:
                seq_lines.append(line.strip())

        # flush last record
        if header is not None:
            seq = "".join(seq_lines).replace(" ", "")
            pct = gc_percent(seq)
            fout.write(f"{header} GC:{pct:.1f}%\n")
            for sl in seq_lines:
                fout.write(sl + "\n")
            written += 1

    return written

def main():
    ap = argparse.ArgumentParser(
        description="Append GC%% to each FASTA header and write a new file."
    )
    ap.add_argument("input", help="Input FASTA/FNA file")
    ap.add_argument("output", help="Output FASTA/FNA file")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        raise SystemExit(f"❌ Input file not found: {in_path}")

    count = process(in_path, out_path)
    print(f"✅ Wrote {count} sequences with GC% → {out_path.resolve()}")

if __name__ == "__main__":
    main()
# find_seq_line.py
import sys
from pathlib import Path

def parse_id_from_header(line: str) -> str:
    # line starts with '>'
    return line[1:].strip().split()[0] if line.startswith(">") else ""

def main():
    if len(sys.argv) != 3:
        print("Usage: python find_seq_line.py <input.fasta> <sequence_id>")
        sys.exit(1)

    fasta_path = Path(sys.argv[1])
    target_id = sys.argv[2]

    if not fasta_path.exists():
        print(f"❌ Input file not found: {fasta_path}")
        sys.exit(1)

    hits = []
    current_is_target = False

    with fasta_path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            s = line.rstrip("\n")

            if s.startswith(">"):
                # new record; check its ID
                current_is_target = (parse_id_from_header(s) == target_id)
                continue

            # sequence/blank line
            if current_is_target:
                if s.strip() == "":
                    # skip blank lines between header and sequence, if any
                    continue
                # first sequence line for this target record
                hits.append(lineno)
                current_is_target = False  # stop collecting until next header

    if hits:
        # If multiple records share the same ID (rare but possible), print all.
        for n in hits:
            print(n)
        sys.exit(0)
    else:
        print(f"❗ ID '{target_id}' not found in {fasta_path.name}")
        sys.exit(2)

if __name__ == "__main__":
    main()



    #!/usr/bin/env python3
from pathlib import Path
import argparse
import sys

def find_sequence_start_line(fasta_path: Path, target_id: str) -> int | None:
    """
    Return the 1-based line number where the *sequence* starts for the entry
    whose header ID matches `target_id`. The ID is taken as the first token
    after '>' on the header line. Skips blank lines between header and sequence.
    """
    header_found = False
    with fasta_path.open("r", encoding="utf-8") as fh:
        for idx, raw in enumerate(fh, start=1):  # 1-based line numbers
            line = raw.rstrip("\n")
            if line.startswith(">"):
                # Parse ID = first whitespace-delimited token after '>'
                id_token = line[1:].strip().split()[0] if len(line) > 1 else ""
                header_found = (id_token == target_id)
            else:
                if header_found:
                    # Skip possible empty lines between header and sequence
                    if line.strip() == "":
                        continue
                    return idx
    return None  # not found

def parse_args():
    ap = argparse.ArgumentParser(
        description="Print the line number where a FASTA sequence starts for a given ID."
    )
    ap.add_argument("fasta", type=Path, help="Input FASTA file")
    ap.add_argument("seq_id", help="Sequence ID to search (first token after '>')")
    return ap.parse_args()

def main():
    args = parse_args()

    if not args.fasta.exists():
        print(f"❌ Input file not found: {args.fasta}", file=sys.stderr)
        sys.exit(1)

    line_no = find_sequence_start_line(args.fasta, args.seq_id)
    if line_no is None:
        print(f"❌ ID '{args.seq_id}' not found in {args.fasta}", file=sys.stderr)
        sys.exit(2)

    print(line_no)

if __name__ == "__main__":
    main()

##!/usr/bin/env python3
from pathlib import Path
import argparse

def parse_args():
    ap = argparse.ArgumentParser(description="Describe what this script does.")
    ap.add_argument("input",  type=Path, help="Input file")
    ap.add_argument("output", type=Path, help="Output file")
    return ap.parse_args()

def main():
    args = parse_args()
    in_path: Path = args.input
    out_path: Path = args.output

    # 例：读 -> 写
    text = in_path.read_text(encoding="utf-8")
    out_path.write_text(text, encoding="utf-8")
    print(f"Done -> {out_path.resolve()}")

if __name__ == "__main__":
    main()


#%% 4.6 Convert FASTQ -> FASTA — robust 4-line parsing (with fallback demo)
# fastq_to_fasta.py
import sys
from pathlib import Path
import gzip

def open_text_maybe_gz(path):
    p = Path(path)
    if p.suffix == ".gz":
        return gzip.open(p, "rt", encoding="utf-8", newline="")
    return open(p, "r", encoding="utf-8", newline="")

def write_fasta_record(fout, header, seq):
    # header: whole header after '@' (keep any trailing info)
    fout.write(">" + header + "\n")
    # write sequence on one line; if you prefer wrapping, split every 60 chars
    fout.write(seq + "\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python fastq_to_fasta.py input.fastq[.gz] output.fasta", file=sys.stderr)
        sys.exit(1)

    fin_path, fout_path = sys.argv[1], sys.argv[2]
    if not Path(fin_path).exists():
        print(f"❌ Input file not found: {fin_path}", file=sys.stderr)
        sys.exit(1)

    records = 0
    with open_text_maybe_gz(fin_path) as fin, open(fout_path, "w", encoding="utf-8", newline="") as fout:
        header = seq = plus = qual = None

        for i, raw in enumerate(fin):
            line = raw.rstrip("\n")

            mod = i % 4
            if mod == 0:
                # Header line: must start with '@'
                if not line.startswith("@"):
                    print(f"❌ Malformed FASTQ at line {i+1}: header must start with '@'", file=sys.stderr)
                    sys.exit(2)
                header = line[1:].strip()  # drop '@'
            elif mod == 1:
                # Sequence line
                seq = line.strip()
            elif mod == 2:
                # Plus line: must start with '+'
                if not line.startswith("+"):
                    print(f"❌ Malformed FASTQ at line {i+1}: third line must start with '+'", file=sys.stderr)
                    sys.exit(2)
                plus = line
            else:
                # Quality line
                qual = line.rstrip()
                # Validate lengths
                if len(seq) != len(qual):
                    print(
                        f"❌ Length mismatch at record {records+1}: "
                        f"seq={len(seq)} vs qual={len(qual)}", file=sys.stderr
                        
                    )
                    sys.exit(2)

                # We have a full record → write FASTA
                write_fasta_record(fout, header, seq)
                records += 1
                # reset (optional)
                header = seq = plus = qual = None

        # If file ended mid-record (not multiple of 4 lines)
        if (i + 1) % 4 != 0:
            print("❌ Incomplete FASTQ: file ended mid-record", file=sys.stderr)
            sys.exit(2)

    print(f"✅ Converted {records} records → {Path(fout_path).resolve()}")

if __name__ == "__main__":
    main()
#%%python fastq_to_fasta.py reads.fastq output.fasta
# or with gzip input:
#python fastq_to_fasta.py reads.fastq.gz output.fasta
