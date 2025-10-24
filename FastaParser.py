#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastaParser.py

Description:
    This program reads a GeneticData text file, cleans and standardizes sequences,
    and writes two FASTA outputs: one for mtDNA and one for Y-chromosome sequences.
    The parser auto-detects common formats (FASTA-like headers, delimited tables,
    and block-style records), replaces invalid symbols with 'N', retains '?' (uncertain)
    and '-' (gap), removes duplicate names (keep first), and produces a QC summary.

User-defined functions:
    clean_seq(rawseq, qc)
        Clean and normalize a raw sequence string: uppercase, normalize non-standard
        characters (—/–/− -> '-', '？' -> '?'), keep only A/C/G/T/N/?/-, and convert 
        other symbols to 'N'. Record QC changes.
    write_fasta(path, entries)
        Write (name, sequence) entries to a FASTA file, 80 chars per line, skipping empty sequences.
    parse_fasta_like(lines, qc)
        Detect and extract sequences from FASTA-style headers: >Name|TYPE=mtDNA or >Name|TYPE=Y.
    parse_table(lines, qc)
        Detect and extract sequences from delimited tables (CSV/TSV/; separated by several types). 
        Column headers should include a name column (name/sample/id), and at least one of
        mtDNA / Y columns.
    parse_block(lines, qc)
        Detect and extract sequences from block-style records like:
            <Sample Name>
            [phenotype/comment...]
            mtDNA
            <sequence possibly containing multiple lines>
            Y chromosome
            <sequence possibly containing multiple lines>
    keep_first(records, qc)
        Remove duplicated entries by name, keeping the first occurrence of individual.
    summarize(records, label, qc)
        Summarize length range and whether all sequences are aligned.
    count_chars(records)
        Return base counts (A/C/G/T/N/?/-) with the list of name and sequence.

Procedure:
    1) Read the input file and try parsers in following order:
       first FASTA-like,then delimited table,then block-style (multi-line).
    2) Clean sequences; keep only A/C/G/T/N/?/-; convert other characters to 'N'.
    3) Drop duplicate names,keep only the first entry.
    4) Write outputs to mtDNA.fasta and Y.fasta.
    5) Write QC summary (format detected, invalid character changes, empties, 
      duplicates, length of alignment, and base total counts).

Inputs:
    GeneticData - 1-9.txt  — raw genetic data for all individuals tested.

Outputs: each input file will output:
    mtDNA.fasta      — FASTA containing mtDNA sequences.
    Y.fasta          — FASTA containing Y sequences.
    parser_log.txt   — QC and parsing summary.

Usage:
    python FastaParser.py INPUT_TXT OUT_MT_FASTA OUT_Y_FASTA

Exit codes:
    0  success
    1  input file not found
    2  bad arguments  or unsupported format (written in parser_log.txt)

Version: 1.00
Date:    2025-10-23
Author:  Yiran Chen 
"""
#%% importing modules
from __future__ import annotations #make type annotation not be evaluated
import sys
import os
import re
import csv
from pathlib import Path
from typing import List, Tuple, Optional #give type hints

#%% Global definition of allowed characters
ALLOWED = set("ACGTN?-")  # Allowed symbols: bases A,C,G,T, N (unknown), ? (uncertain); - (gap)

# %% the function of cleaning and normalization rawdata
def clean_seq(rawseq: str | None, qc: dict) -> str:
    s = (rawseq or "").strip().upper() #if the rawseq are empty, use ""(an empty string)
    s = (s #normalize these look-alike characters to standard ASCII
         .replace("—", "-")
         .replace("–", "-")
         .replace("−", "-")
         .replace("？", "?")
         )

    cleaned = [] #create a cleaned list for sequences
    changed = 0 #counter for replaced invalid symbols
    for ch in s:
        if ch in ALLOWED:
            cleaned.append(ch) #added valid characters to the cleaned data list
        elif ch in "\t\r\n ": #all kinds of whitespaces will be skiped
            continue
        else:
            cleaned.append("N") #other not valid characters changed to N
            changed += 1 #update counts

    if changed:
        qc["non_acgtn_symbols_converted"] += changed #update qc dictionary
    return "".join(cleaned) #join the valid characters to single cleaned string

#%% the function of write cleaned sequences to fasta file
'''
 path : str | Path
        The output file path for fasta files.
        str（like "outputs/mtDNA_1.fasta") or a pathlib.Path object(like Path("outputs") / "mtDNA_1.fasta")
        are both allowed.
p.parent.mkdir(parents=True, exist_ok=True)
        The function will automatically create the parent directory if it does not exis
entries : List[Tuple[str, str]]
        A list of (name, sequence) pairs, 
        and the name is in str format as FASTA header, the sequences are also cleaned sequences in str format.
        Example:
            [
                ("Princess Irene", "ACGTTG--A?CT"),
                ("Prince Fred", "ACGTTG--A?CT")
            ]
'''
def write_fasta(path: str | Path, entries: List[Tuple[str, str]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for name, seq in entries:
            if not seq: #skip empty sequences
                continue
            f.write(f">{name}\n") #write headers
            for i in range(0, len(seq), 80): #keep 80 characters for one single line
                f.write(seq[i:i+80] + "\n")

#%% Parse DNA sequences from a FASTA-like formatted text.
def parse_fasta_like(lines: List[str], qc: dict):
#lines : List[str]:List of strings representing the lines of the input file.
# qc : dict: A dictionary for tracking quality control metrics (format_detected, empty records).
    header_re = re.compile(r"^>([^|\r\n]+)\|TYPE=(mtDNA|Y)$", re.I)
    #match headers like  >SampleName|TYPE=mtDNA or >SampleName|TYPE=Y
    mt, yy = [], [] #output separately for mtdna and y chromosome dna
    cur_name: Optional[str] = None #The name (header) of the current sequence being read.
    cur_type: Optional[str] = None #The type of the current sequence, extracted from the header ("mtDNA" or "Y").
    cur_buf: List[str] = []#A temporary list buffer used to collect all sequence lines for the current record.
    seen_any = False# A Boolean flag indicating whether at least one FASTA header ('>') has been found.
    for ln in lines:
        m = header_re.match(ln.strip()) #remove whitespaces and find if there are matched header
        if m:
            seen_any = True #at least one valid FASTA header in this file
            if cur_name is not None and cur_type is not None:
            # If there is already a previous record, store it and join beffered sequences, and separate mt or Y
                seq = clean_seq("".join(cur_buf), qc)
                (mt if cur_type.lower() == "mtdna" else yy).append((cur_name, seq))
            cur_name = m.group(1).strip()
            cur_type = m.group(2)
            cur_buf = []
            #Start a new entry from this header:
            #group(1) = sample name, group(2) = type ('mtDNA' or 'Y')
            #Reset the sequence buffer for the new entry
        else:
            if cur_name is not None:
                cur_buf.append(ln.strip())
            #If an entry name is now found, add the segments of sequences all together
    if cur_name is not None and cur_type is not None:
        seq = clean_seq("".join(cur_buf), qc)
        (mt if cur_type.lower() == "mtdna" else yy).append((cur_name, seq))
    #The first round of loop there is no valid header before, so add the last one manully
    if seen_any:
        qc["format_detected"] = "FASTA-like"
        return mt, yy
    #If at least one header found used this parser, update qc about format and return results
    return None, None
    #No FASTA-like headers were found and record this parser is not used
