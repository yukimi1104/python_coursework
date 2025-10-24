#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastaParser.py
Description:
    This program reads a GeneticData text file(our group is file-6), cleans and 
    standardizes DNA sequences,and outputs two FASTA files: one for mtDNA and 
    one for Y-chromosome sequences.
    The parser automatically detects multiple types of common formats:
        - FASTA-like headers (e.g., >Name|TYPE=mtDNA)
        - Delimited tables (CSV/TSV/semicolon/pipe)
        - Block-style records (Name → mtDNA → sequence → Y chromosome → sequence)
    Invalid symbols are converted to 'N', while '?' (uncertain base) and '-' (gap)
    are preserved. Duplicate names are removed, keeping the first entry, and
    QC check result is also summarized.
User-defined functions:
    clean_seq(raw)
       Standardize a raw sequence string: convert to uppercase, replace similar
        symbols (—/–/− → '-', '？' → '?'), keep only A/C/G/T/N/?/-, and replace
        all other symbols with 'N'.
    write_fasta(path, entries)
        Write (name, sequence) pairs to a FASTA file (80 characters per line),
        skipping empty entries.
    parse_fasta_like(lines)
        Extract sequences from FASTA-style headers:
        >Name|TYPE=mtDNA or >Name|TYPE=Y.
    parse_table(lines)
        Detect and extract sequences from delimited tables (CSV, TSV, semicolon,
        or pipe-separated). The table must contain a name column and
        at least one ggene sequence column (mtDNA or Y).
    parse_block(lines)
        Detect and extract sequences from block-style records of the form:
            <Sample Name>
            [optional phenotype/comment]
            mtDNA
            <multi-line sequence>
            Y chromosome
            <multi-line sequence>
    keep_first(records)
        Remove duplicated entries by name, keeping the first occurrence.
    summarize(records, label, qc)
        Summarize the number of sequences, length range, and how well the alignments are.
    count_chars(records)
        Calculate total counts of A/C/G/T/N/?/- and total base length across sequences.
Procedure:
    1) Read the input text file and try parsers in this order:
         FASTA-like → delimited table → block-style.
    2) Clean all sequences to retain only valid symbols (A/C/G/T/N/?/-).
    3) Remove duplicate names, keeping the first entry of each individual.
    4) Write two FASTA outputs:
         <output_prefix>_mtDNA.fasta
         <output_prefix>_Y.fasta
    5) Print a QC summary including detected format, invalid symbol conversions,
       empty sequences, duplicates removed, sequence lengths, and total base counts.
Inputs:
    GeneticData - [group number].txt — raw genetic data for multiple individuals.
Outputs:
    <output_prefix>_mtDNA.fasta  — cleaned mtDNA sequences.
    <output_prefix>_Y.fasta      — cleaned Y-chromosome sequences.
Usage:
    python FastaParser.py INPUT_TXT OUTPUT_PREFIX
Example:
    python FastaParser.py "GeneticData - 6.txt" outputs/Group6
Exit codes:
    0  success
    1  input file not found
    2  unsupported or unrecognized input format
Version: 1.0
Date:    2025-10-24
Author:  Yiran Chen
"""
#%% importing library
from __future__ import annotations # postpone evaluation of type hints; store them as strings.
from typing import List, Tuple, Optional # static typing helpers.
from pathlib import Path  # object-oriented filesystem paths.
import sys  # intepreter utility(e.g., argv, exit).
import os   # OS interfaces (paths,etc).
import csv  # CSV parsing and writing.
import re   # regular expressions.
#%% global definition of allowed character set
ALLOWED = set("ACGTN?-")
#%% the function of clean raw sequence data
def clean_seq(raw: str|None) -> str:
    s = (raw or "").strip().upper() #remove whitespace and upper all letters
    s = (s.replace("—","-").replace("–","-").replace("−","-").replace("？","?"))#change similar symbols to standard ones
    out = [] #initialize one empty out list
    for ch in s: #iterate through
        if ch in ALLOWED:
            out.append(ch) #add valid characters to cleaned output
        elif ch in "\t\r\n ": #skip whitespaces
            continue
        else:   #other not valid characters output as "N"
            out.append("N")
    return "".join(out) #join the segment of cleaned data together
#%% the function of writing (name, sequence) pairs to a FASTA file 
def write_fasta(path: str|Path, entries: List[Tuple[str,str]]) -> None:
    p = Path(path) #convert string or os.PathLike to a Path object
    p.parent.mkdir(parents=True, exist_ok=True) #ensure the parent directory exists (no error if already exists)
    with p.open("w", encoding="utf-8") as f:
        for name, seq in entries:
            if not name or not seq: #skip the empty lines which without sample name or dna sequences
                continue 
            f.write(f">{name}\n") #write out the output file
            for i in range(0, len(seq), 80):#keep it to 80 characters per line
                f.write(seq[i:i+80] + "\n")
#%% the function of recognizing duplications and renaming duplicated ones
def dedup_rename(records: List[Tuple[str,str]]) -> List[Tuple[str,str]]:
    counts = {} #initiate empty count of name and output
    out = [] 
    for name, seq in records:
        if not name: #skip empty sample id
            continue
        if name in counts: #if id name already exists, update duplication count
            counts[name] += 1
            new_name = f"{name}_{counts[name]}" #like anastasia_002, if have alike duplications
        else:
            counts[name] = 1 
            new_name = name #keep the original name
        out.append((new_name, seq))
    return out
#%% three parser functions(fasta-like / table / block) 
header_re = re.compile(r"^>([^|\r\n]+)\|TYPE=(mtDNA|Y)$", re.I) #match with start with ">" and with TYPE=mtdna or Y
def parse_fasta_like(lines: List[str]):
    mt, yy = [], [] #initiate empty list for mtdna and y chromosome
    cur_name: Optional[str] = None #current name, can be none
    cur_type: Optional[str] = None #current type(mtdna, y),can be none
    cur_buf: List[str] = [] #buffer for the current sequence's chunks (collect lines until finish this entry)
    seen = False #parser state indicator to avoid emitting empty records before the first valid entry
    for ln in lines:
        m = header_re.match(ln.strip()) #check if this line is a header using the regex
        if m:
            seen = True #mark there are at least one valid line with name and seq
            if cur_name and cur_type: #processing with the previous record before moving to next
                seq = clean_seq("".join(cur_buf)) #join buffered segments together
                (mt if cur_type.lower()=="mtdna" else yy).append((cur_name, seq)) #assigned to different types
            # initialize a new record from the header capture groups
            cur_name = m.group(1).strip()#split the line into sample name and type
            cur_type = m.group(2)
            cur_buf = [] #clear the buffer
        else:
            if cur_name is not None: #not a header line: if inside a record, accumulate sequence content.
                cur_buf.append(ln.strip()) #added the buffer sequences to already exists entry
    if cur_name and cur_type: #commit if there are pending buffers
        seq = clean_seq("".join(cur_buf))
        (mt if cur_type.lower()=="mtdna" else yy).append((cur_name, seq))
    return (mt, yy) if seen else (None, None)#if no headers were seen at all, indicate that nothing was parsed.
#the parser for tables
def parse_table(lines: List[str]):
    text = "".join(lines) #rebuild the full text; splitlines() below will handle any newline style.
    for delim in [",", "\t", ";", "|"]:
        try:
            rows = list(csv.reader(text.splitlines(), delimiter=delim)) #split rows by dilimiter
            if not rows:  #skip empty rows
                continue
            headers = [h.strip().lower() for h in rows[0]] #normalize header cells for robust matching (trim + lowercase)
            name_idx = mt_idx = y_idx = None #placeholders for column indices
            for i, h in enumerate(headers):#like 0,name;1,mtdna;2,ydna
                if name_idx is None and (h in ("name","sample","id") or "name" in h or "sample" in h): #several possible expressions for sample id
                    name_idx = i 
                if mt_idx is None and "mtdna" in h: #several possible expressions for mtdna
                    mt_idx = i
                if y_idx is None and (
                    h == "y" or "y_dna" in h or "ychrom" in h or "y-chrom" in h
                    or h == "ychromosome" or h == "y chromosome"
                ):
                    y_idx = i
            if name_idx is None or (mt_idx is None and y_idx is None):#if this delimiter guess fails,try the next one.
                continue
            mt, yy = [], [] #accumulator for parsed (name, sequence) pairs by type.
            for r in rows[1:]: #iterate over data rows (skip the header at index 0)
                if not r: 
                    continue
                name = (r[name_idx] if name_idx < len(r) else "").strip() #name colomun number must less than the row length
                if not name: 
                    continue
                if mt_idx is not None and mt_idx < len(r):
                    seq_mt = clean_seq(r[mt_idx]) 
                    if seq_mt: mt.append((name, seq_mt)) #append (name, mtDNA) to the accumulator.
                if y_idx is not None and y_idx < len(r):
                    seq_y = clean_seq(r[y_idx]) 
                    if seq_y: yy.append((name, seq_y)) #append (name, Y-DNA) to the accumulator
            return mt, yy
        except Exception: #parsing failed under this delimiter speculation,try the next candidate
            continue
    return None, None #no usable delimiter detected across all candidates
#%% the parser for block-style fasta-like files
def parse_block(lines: List[str]):
    # treat several variants as types and ignore phenotype lines as names
    def is_mt_title(s: str) -> bool:
        low = s.lower().strip() 
        return low in ("mtdna", "mt dna", "mitochondrial dna") #common mtDNA block titles
    def is_y_title(s: str) -> bool:
        low = s.lower().strip()
        return low in ("y chromosome","y-chromosome","ychromosome","y")#common Y-chromosome titles
    def is_phenotype(s: str) -> bool:
        low = s.lower().strip() #phenotype about hemophilia
        return low.startswith("a hemophilia") or low.startswith("not a hemophilia") 
        #phenotype annotations should not be treated as sample names
    def norm_name(s: str) -> str:
        s = s.strip()
        if s.startswith(">"):   
            s = s[1:].strip() #remove ">" before name
        return s
    def flush(buf: List[str]) -> str: #join buffered sequence fragments, trim whitespace, then clean data
        return clean_seq("".join(part.strip() for part in buf if part.strip()))
    #initialize placeholder for mtdna and ydna
    mt, yy = [], [] #accumulators for parsed (name, sequence) tuples: mtDNA -> mt, Y-DNA -> yy
    name: Optional[str] = None # current sample name being processed; none means no active sample yet.
    mode: Optional[str] = None # current block type: "mt" for mtDNA, "y" for Y-DNA, or None when not in a block.
    buf: List[str] = [] # line buffer for sequence fragments until commiting a record
    def commit():
        nonlocal buf, mode, name # mutate the outer-scope variables declared above
        if not name or not mode:
            buf.clear(); mode = None; return  #incomplete record (missing name or type): reset and do nothing.
        seq = flush(buf)#join + clean buffered sequence fragments via flush() to clean_seq( )
        if seq:
            (mt if mode=="mt" else yy).append((name, seq)) #append (name, sequence) to the proper accumulator.
        buf.clear(); mode = None #reset the buffer and exit block mode for the next record.
    #iterate over each raw input line.
    for raw in lines:
        s = raw.strip()
        if not s:
            commit() #finalize any pending record before resetting contextual state
            continue
        # titles
        if is_mt_title(s): #check line for block header types
            commit(); mode = "mt"; continue # flush previous record, enter mtDNA mode
        if is_y_title(s):
            commit(); mode = "y";continue
        # inside sequence collection
        if mode in ("mt","y"):
            buf.append(s); continue
        if is_phenotype(s):
            #treat phenotype not as name
            continue
        # treat as a (new) sample name
        name = norm_name(s)
    commit()
    return (mt, yy) if (mt or yy) else (None, None)
#%% main function
def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: python FastaParser.py text_file output_fasta_file\n")
        sys.exit(2) #exit code 2: command-line usage error
    in_txt = sys.argv[1] #path for input file
    out_prefix = sys.argv[2] #path for output file
    if not os.path.isfile(in_txt): # existence check for the input file.
        sys.stderr.write(f"[ERROR] Input not found: {in_txt}\n"); sys.exit(1)
    #read the entire input as lines 
    with open(in_txt, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    mt, yy = parse_fasta_like(lines) # parsing as a FASTA-like format first
    if mt is None and yy is None:
        mt, yy = parse_table(lines)#try parsing as a delimited table
    if mt is None and yy is None:
        mt, yy = parse_block(lines)#try parsing as a block
    if mt is None and yy is None:
        sys.stderr.write("[ERROR] Could not detect input format.\n"); sys.exit(2)
        #if all parsers failed, report an error and stop.
    # returns a list of (name, sequence) with unique names.
    mt = dedup_rename(mt)
    yy = dedup_rename(yy)
    out_mt = f"{out_prefix}_mtDNA.fasta"
    out_y  = f"{out_prefix}_Y.fasta"
    write_fasta(out_mt, mt)
    write_fasta(out_y, yy)
    print(f"[OK] Wrote: {out_mt} and {out_y}") #print successful message
#Standard Python entry point guard
if __name__ == "__main__":
    main()

