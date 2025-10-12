# -*- coding: utf-8 -*-
"""
Date: 2025-10-12
Author: YIranChen

Description:
  5. Functions — Spyder-style cells. Simple, readable, and in-class Python only.

Usage:
  Run cell-by-cell with Ctrl+Enter.
"""

#%% 5.1 A one-liner function that prints a line
def print_line():
    print("This is a function!")

# Demo
# print_line()


#%% 5.2 Return the string instead of printing
def get_line():
    return "This is a function!"

# Demo
# result = get_line()
# print(result)
# print(result[0])


#%% 5.3 Greet two names
def greet(name1, name2):
    return f"Hello {name1} and {name2}!"

# Demo
# print(greet("Björn", "Dag"))


#%% 5.4 Greet with optional names (default to '?')
def greet_opt(name1="?", name2="?"):
    return f"Hello {name1} and {name2}!"
# Demo
# print(greet_opt())
# print(greet_opt("Petr"))
# print(greet_opt("Björn", "Dag"))


#%% 5.5 Two separate functions: add and multiply
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# Demo
# print(multiply(2, 3))  # 6
# print(add(2, 3))       # 5


#%% 5.6 One function that chooses operation
def calculate(a, b, operation="add"):
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    else:
        raise ValueError("operation must be 'add' or 'multiply'")
m=calculate(2,3,operation="multiply")
print(m)

# Demo
# print(calculate(2, 3, operation="add"))       # 5
# print(calculate(2, 3, operation="multiply"))  # 6


#%% 5.7 GC-content of a nucleotide string (return fraction)
def get_gc(seq):
    s = seq.upper()
    if not s:
        return 0.0
    gc = s.count("G") + s.count("C")
    return gc / len(s)

# Demo
# print(get_gc("CACAGGTT"))  # 0.5
# print(get_gc("CAG"))       # 0.6666...


#%% 5.8 Print "Hi!" n times (obnoxious)
def many_hi_print(n):
    for _ in range(n):
        print("Hi!")

# Demo
# many_hi_print(4)


#%% 5.9 Return a list with n times "Hi!"
def many_hi(n):
    return ["Hi!" for _ in range(n)]
def many_hi(n):
    hi_list=[]
    for i in range(n):
        hi_list.append("Hi!")
    return hi_list

# Demo
# hi_list = many_hi(6)
# print(hi_list)


#%% 5.10 Add optional parameter 'word' (default "Hi!")
def many_word(n, word="Hi"):
    return [f"{word}!" for _ in range(n)]

# Demo
# print(many_word(3))                # ["Hi!", "Hi!", "Hi!"]
# print(many_word(4, word="Halloa")) # ["Halloa!",...]


#%% 5.11 Build a FASTA dictionary (IDs as keys, sequences as values)
# Single-line FASTA example (copy/paste-friendly)
fasta_dict = {
    "header1.1": "ATGCTAGCTAGCTAGCTACG",
    "header1.2": "ACGTAGCTAGCTAGCAC",
    "header2.1": "AGCTAGCTAGCTATTATCTACT"
}

# Demo
# print(fasta_dict)


#%% 5.12 Iterate FASTA dict and print messages (in insertion order)
def print_fasta_entries(fd):
    idx = 1
    for hdr in fd:
        seq = fd[hdr]
        print(f"Entry {idx} has header: {hdr} and sequence: {seq}")
        idx += 1

# Demo
# print_fasta_entries(fasta_dict)


#%% 5.13 Load FASTA (single-line format) from file path -> dict
# Assumptions:
# - Headers start with '>'
# - Each sequence is on a single line (no wrapping)
def load_fasta(path):
    result = {}
    header = None
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                header = line[1:].strip()
                result[header] = ""  # prepare slot
            else:
                # single-line format: entire sequence on one line
                if header is not None:
                    result[header] = line
    return result

# Demo (uncomment if you have sequences.fasta file next to this script)
# fasta_dict_from_file = load_fasta("sequences.fasta")
# print(fasta_dict_from_file)


#%% 5.14 Calculate GC-content for each sequence in sequences.fasta
def calcGC(seq):
    s = seq.upper()
    if not s:
        return 0.0
    return (s.count("G") + s.count("C")) / len(s)

# Example pipeline:
# 1) Load sequences
# 2) Save all sequences to a list
# 3) Iterate and print GC values

# Safe demo: try real file, else fall back to the example dict from 5.11
def gc_report_from_fasta(path="sequences.fasta"):
    try:
        fd = load_fasta(path)
        if not fd:
            # empty file or wrong format -> fallback
            fd = fasta_dict
    except FileNotFoundError:
        fd = fasta_dict

    sequenceList = list(fd.values())
    for sequence in sequenceList:
        gc = calcGC(sequence)
        print(f"{sequence}: {gc}")
