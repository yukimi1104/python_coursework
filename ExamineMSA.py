#!/usr/bin/env python3
"""
ExamineMSA.py

Description
-----------
Compute pairwise statistics for all sequence pairs in an aligned FASTA file:
- Comparable count: columns where both sides have valid A,C,T,G
- Uncertain count : columns where at least one base is N, ? or '-'
- Total length    : full alignment length
- Identity%       : 100 * (# identical A/C/G/T matches) / TOTAL columns
- Score           : per-column sum using weights:
                      MATCH     (+1 default)   when A/C/G/T == A/C/G/T
                      MISMATCH  (-1 default)   when A/C/G/T != A/C/G/T
                      GAP       (-2 default)   when any '-' appears
                      UNKNOWN   ( 0 default)   when any '?' or 'N' (and no gap)

Procedure
1) Read the fasta file and extract name and sequences.
2) Clean sequences to keep only `ACGTN?-`; anything else character→ 'N'.
3) Check the number of sequences, must be no less than 2
4) Verify all sequences have identical length; if not aligned, exit with code 3.
5) Load scoring weights:
   - If <weights_file> is "-" or missing, use defaults {MATCH=1, MISMATCH=-1, GAP=-2, UNKNOWN=0}.
   - Otherwise parse KEY=VALUE lines; invalid lines are ignored.
6) For each pair (i < j), compute:
   - comparable, uncertain, total, Identity% (over TOTAL), and Score (weighted sum).
7) Write results to the specified output file with a header row.

User-defined functions
-   read_fasta(path: str | Path) -> List[Tuple[str, str]]
    Read an aligned FASTA into a list of name and sequences and clean data
-   load_weights(path: str | Path) -> Dict[str, float]
    Load scoring weights from user provided weights.tsv, get values for keys("match","mismatch","gap","unknown")
    Returns defaults when path is not available. 
-   check_aligned(recs: List[Tuple[str, str]]) -> int
    Ensure all sequences share the same length; returns that alignment length.
    Raises `ValueError` if lengths differ.
-   pair_stats(a: str, b: str, w: Dict[str, float]) -> Tuple[int, int, int, float, float]
    Compute pairwise metrics for two aligned sequences:
    (comparable, uncertain, total, identity_pct, score)

Inputs
- <fasta_file>       : aligned FASTA with at least two sequences
- <weights_file_or_->: path to weights file or using default settings
- <output_file>      : path to write the pairwise table

Outputs
- A table with columns and scores:
   SampleA | SampleB | Comparable | Uncertain | Total | Identity% | Score

Usage
     python ExamineMSA.py <fasta_file> <weights_file_or_-> <output_file>

Examples
   python ExamineMSA.py outputs/Group6_mtDNA.fasta - outputs/mtDNA_6_pairwise.tsv
   python ExamineMSA.py outputs/Group6_Y.fasta weights.tsv outputs/Y_6_pairwise.tsv

Exit codes
0 : success
1 : FASTA not found or unreadable
2 : usage error or fewer than 2 sequences
3 : sequences not aligned (lengths differ)

Version: 1.0
Date   : 2025-10-24
Author : Yiran Chen

"""
#%% importing library
from __future__ import annotations #postpone evaluation of type hints.
from typing import List, Tuple, Dict #static typing helpers
from pathlib import Path #object-oriented filesystem paths
import sys #intepreter utility(e.g., argv, exit).
#%% global definition of allowed character set
ALLOWED = set("ACGTN?-")
#%% the function of read aligned fasta file to (name,sequence) tuple
def read_fasta(path: str|Path) -> List[Tuple[str,str]]:
    name = None # current header (without '>'); None means no active header now
    buf: List[str] = [] #accumulator for sequence lines of the current record.
    out: List[Tuple[str,str]] = [] #final output of tuple(name,sequence)
    with open(path, "r", encoding="utf-8") as f:
        for ln in f: #iterate lines
            ln = ln.rstrip("\n")
            if ln.startswith(">"):#headerlines with names
                if name is not None: #there is a previous record, flush it first.
                    out.append((name, "".join(buf)))
                name = ln[1:].strip() #remove ">" and get name
                buf = [] #clean buffer seqs
            else:
                buf.append(ln.strip().upper()) #if not headerline, added to buffer list
        if name is not None:
            out.append((name, "".join(buf))) #commit the last buffer sequencing
    # keep only allowed characters
    out = [(n, "".join(ch if ch in ALLOWED else "N" for ch in s)) for n,s in out]
    return out
#%% the function of loading scoring weights through optional file or default
def load_weights(path: str|Path) -> Dict[str, float]:
    # define key-value dict
    w = {"MATCH":1.0, "MISMATCH":-1.0, "GAP":-2.0, "UNKNOWN":0.0}
    if path and Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip() #remove whitespace
                if not ln or ln.startswith("#") or "=" not in ln: #check if file not empty and have key-value "="
                    continue
                k,v = ln.split("=",1) #get values 
                try:
                    w[k.strip().upper()] = float(v.strip())
                except ValueError:
                    pass #ignore lines where VALUE is not a valid float
    return w #return checked key-values
#%% the function of checking all sequences have identical length
def check_aligned(recs: List[Tuple[str,str]]) -> int:
    lengths = {len(s) for _,s in recs}
    if len(lengths) != 1: #more than one sequence length → not aligned.
        raise ValueError(f"Sequences not aligned (lengths found: {sorted(lengths)})")
    return next(iter(lengths)) #return the single common length
#%% the function of calculating pairwise stats between two aligned sequences
def pair_stats(a: str, b: str, w: Dict[str,float]) -> Tuple[int,int,int,float,float]:
    total = len(a) #alignment length (assumed equal to len(b))
    comp = 0 #count of comparable columns (both in A/C/G/T).
    unc  = 0 #count of uncertain columns (any side in N/?/-).
    ident = 0 #count of identical A/C/G/T matches.
    score = 0.0 #accumulating scores
    for x,y in zip(a,b): #iterate pair sequences if valid characters
        ax = x in "ACGT"
        ay = y in "ACGT"
        if ax and ay:#if at the given position, both sides valid
            comp += 1
            if x == y:
                ident += 1 #if identical
                score += w["MATCH"]
            else: #does bot identical
                score += w["MISMATCH"]
        else: #uncertain bases
            # at least one is N/?/-
            unc += 1
            if x == "-" or y == "-": #gap
                score += w["GAP"]
            else: #unknown
                score += w["UNKNOWN"]
    identity_pct = (100.0 * ident / total) if total > 0 else 0.0 #calculate percentage of identity
    return comp, unc, total, identity_pct, score

def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: python ExamineMSA.py fasta_file weight_parameters output_file\n")
        sys.exit(2) #usage error
    fasta_file, weights_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3]
    # Ensure the FASTA exists and is readable; if not, exit with code 1.
    try:
        recs = read_fasta(fasta_file)              
    except FileNotFoundError:
        sys.stderr.write(f"[ERROR] FASTA not found: {fasta_file}\n")
        sys.exit(1)
    except OSError as e:
        sys.stderr.write(f"[ERROR] Could not read FASTA: {fasta_file} ({e})\n")
        sys.exit(1)
    # there should be no less than two sequences to compute pairwise stats.
    if len(recs) < 2:
        sys.stderr.write("[ERROR] Need at least 2 sequences for pairwise comparison.\n")
        sys.exit(2)
    #check all aligned(same length)
    try:
        aln_len = check_aligned(recs)                
    except ValueError as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        sys.exit(3)
    # load scoring weights; "-" (or missing file) keeps defaults.
    W = load_weights(weights_file)
    # prepare the output directory (idempotent: no error if it already exists).
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    # open output file and write a simple header + all pairwise rows.
    with open(out_file, "w", encoding="utf-8") as f:
        # formatting output table header
        f.write("SampleA | SampleB | Comparable | Uncertain | Total | Identity% | Score\n")
        n = len(recs)                                
        for i in range(n):                      #iterate each pair     
            for j in range(i + 1, n):                
                a_name, a_seq = recs[i]              
                b_name, b_seq = recs[j]             
                # compute pairwise statistics under the selected weights.
                comp, unc, tot, ident_pct, sc = pair_stats(a_seq, b_seq, W)
                # formatting output score : integer if exact, else rounded to 3 decimals.
                sc_out = int(sc) if float(sc).is_integer() else round(sc, 3)
                # output line formatting
                f.write(f"{a_name} | {b_name} | {comp} | {unc} | {tot} | {ident_pct:.1f}% | {sc_out}\n")
    # success message to stdout
    print(f"[OK] Aligned length={aln_len}. Wrote: {out_file}")


# Standard Python script entry-point guard.
if __name__ == "__main__":
    main()
