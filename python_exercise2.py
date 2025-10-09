# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 18:40:22 2025

@author: Yiran Chen
"""

"""
Date: 2025-10-07
Author:Yiran CHen

Description:
    Solutions for:
      2. Collection data types: Lists, Sets and Dictionaries
      2.1 Lists
      2.2 Dictionaries
      2.3 Sets

Usage:
    Run cell-by-cell with Ctrl+Enter (Spyder style).
    Cells that normally need input() include a safe fallback so they won't block execution.
"""
#%% 2.1 Lists — 1
# Ask the user for three ingredients and print:
# ['bread','ingredient1','ingredient2','ingredient3','bread']

def three_ingredients():
    try:
        ing1 = input("Ingredient 1: ").strip()
        ing2 = input("Ingredient 2: ").strip()
        ing3 = input("Ingredient 3: ").strip()
        items = ["bread", ing1, ing2, ing3, "bread"]
    except Exception:
        # Safe fallback (non-interactive)
        items = ["bread", "tomato", "cheese", "lettuce", "bread"]
    print(items)

three_ingredients()

#%% 2.1 Lists — 2
# Use input() to get comma-separated numbers, compute sum, print to stdout.

def sum_from_input():
    try:
        s = input("numbers by comma: ").strip()
    except:
        # fallback if input fails (e.g., non-interactive mode)
        print("Input failed, using default values.")
        s = "1, 11, 1"

    nums = []  # create empty list

    for part in s.split(","):
        part = part.strip()
        if part:
            try:
                nums.append(float(part))
            except ValueError:
                print(f"Skipped invalid value: {part}")

    print("Numbers list:", nums)
    print("Sum:", sum(nums))

sum_from_input()
  

#%% 2.1 Lists — 3
# Load codon line as a single string, make a list of codons (uniform case).

codon_line = """AAA AAT AAC aag ATA ATT ATC ATG Aca ACT ACC Acg AGA AGT AGC agG TAA TAT TAC TAG
TTA TTT TTC TTG TCA tct TCC tCg TGA TGT TGC TGG CAA CAT CAC CAG CTA cTT ctc CTG
CCA CCT CCc CCG CGA CGT CGC cgg GAA GAT GAC GAG GTa GTT GTC GTG GCA GCT GCC GcG
GGA GGT GGC gGG"""

codons = [c.strip().upper() for c in codon_line.split() if c.strip()]
print(len(codons), "codons loaded.")
print(codons[:10], "...")
#codons = []
for c in codon_line.split():
    if c.strip():               # only keep non-empty pieces
        c = c.strip().upper()   # remove spaces, convert to uppercase
        codons.append(c)        # add to the list


##%% 2.1 Lists — 4
# From the list created in the previous exercise, remove all codons that result in Leucine.

# The Leucine codons
LEU_CODONS = {"TTA", "TTG", "CTT", "CTC", "CTA", "CTG"}

# Make a new list that contains all codons except the ones for Leucine
codons_non_leu = [c for c in codons if c not in LEU_CODONS]

# Print results
print("Original codon count:", len(codons))
print("After removing Leucine codons:", len(codons_non_leu))
print("Leucine codons removed:", sorted(list(LEU_CODONS & set(codons))))
print("Example of remaining codons:", codons_non_leu[:10])

print(f"Original codon count: {len(codons)}")
print(f"After removing Leucine codons: {len(codons_non_leu)}")
print(f"Leucine codons removed: {sorted(list(LEU_CODONS & set(codons)))}")
print(f"Example of remaining codons: {codons_non_leu[:10]}")


#%% 2.1 Lists — 5
# Create the same list of codons totally in Python starting with the string 'ATCG'
s=["A","C","T","G"]
codon=[]
for a in s:
    for b in s:
        for c in s:
            codon.append(a+b+c)
print(len(codon))
print(codon)

#%% 2.2 Dictionaries — 1
# Create a fruit dictionary in two ways:
# (1) Start with an empty dictionary and add elements using assignment.
# (2) Start with a populated dictionary using curly braces.

# (1) Empty dictionary first
week_fruits = {}                # create empty dict
week_fruits["apples"] = 4       # add key-value pair
week_fruits["pears"] = 2
week_fruits["oranges"] = 2

print("Dictionary created by assignment:")
print(week_fruits)

# (2) Pre-populated dictionary
week_fruits_alt = {
    "apples": 4,
    "pears": 2,
    "oranges": 2
}

print("\nDictionary created directly:")
print(week_fruits_alt)

#%% 2.2 Dictionaries — 1a
# Update the existing fruit dictionary after buying:
# +2 pears, +5 oranges, +1 watermelon

# Start from the existing dictionary
week_fruits = {"apples": 4, "pears": 2, "oranges": 2}

# Update values using arithmetic operations
week_fruits["pears"] += 2        # 2 + 2 = 4
week_fruits["oranges"] += 5      # 2 + 5 = 7
week_fruits["watermelon"] = 1    # new fruit, so just assign

# Print the updated dictionary
print("Updated fruit counts:")
print(week_fruits)

#%% 2.2 Dictionaries — 1b
# Iterate through the dictionary keys and print the fruit and count on each line.

# Continue from the updated dictionary
week_fruits = {'apples': 4, 'pears': 4, 'oranges': 7, 'watermelon': 1}

# Iterate through the keys
for fruit in week_fruits:
    print(f"{fruit}: {week_fruits[fruit]} pieces")
    
#%% 2.2 Dictionaries — 1c
# Print the fruits and counts, but in alphabetic order of fruit names.

# Continue from the updated dictionary
week_fruits = {'apples': 4, 'pears': 4, 'oranges': 7, 'watermelon': 1}

# Sort the keys alphabetically using sorted()
for fruit in sorted(week_fruits):
    print(f"{fruit}: {week_fruits[fruit]} pieces")
    
#%% 2.2 Dictionaries — 2
# Merge your fruit list with your friend's list and sum the counts for overlapping fruits.

# Your own fruit dictionary
week_fruits = {'apples': 4, 'pears': 4, 'oranges': 7, 'watermelon': 1}

# Friend's dictionary (given one-liner)
friend_week_fruits = {'apples': 2, 'pears': 1, 'oranges': 2, 'waxberry': 4}

# Create a new dictionary containing all unique fruits from both
friend_week_fruits = {
    'apples':2,
    'pears':1,
    'oranges':2,
    'waxberry':4
    }

# Make all key names singular
normalized_friend = {}
for key, value in friend_week_fruits.items():
    if key.endswith("s"):
        #normalized_friend[key[:-1]] = value
        normalized_friend[key.rstrip("s")] = value
    else:
        normalized_friend[key] = value

#print(normalized_friend)

# Combine both dictionaries
fruits_combined = {}

# Add the first dictionary
for key, value in sorted_fruits.items():
    fruits_combined[key] = value

# Add the second dictionary, taking into account the keys that already exist
for key, value in normalized_friend.items():
    if key in fruits_combined:
        fruits_combined[key] += value
    else:
        fruits_combined[key] = value

print(f"My fruit list:")
for key in sorted_fruits: #fruits.value(), fruits.items()
    print(f"{key}: {sorted_fruits[key]} pieces")

print(f"\nMy friend's fruit list:")
for key in friend_week_fruits: #fruits.value(), fruits.items()
    print(f"{key}: {friend_week_fruits[key]} pieces")

print(f"\nThe combined fruits list:")
for key in fruits_combined: #fruits.value(), fruits.items()
    print(f"{key}: {fruits_combined[key]} pieces")


#%% 2.2 Dictionaries — 3
# Make a small tab-separated file (TSV), load it into a dictionary,
# then filter by sequence contents (W and X).

# Create a small TSV file (for demo; in practice, you could load an existing file)
data = """ProteinID\tProteinSeq
prot1\tAGSATGDASD
prot4\tASLWASLD
prot9\tPPASDSADSAD
prot2\tXXSWKJXS
prot8\tPSOASSADASD"""

with open("proteins.tsv", "w") as file:
    file.write(data)
    
print(data)

#%% a) Load the table into a dictionary
protein_seq_dict = {}

with open("proteins.tsv", "r") as file:
    next(file) # Skip the header
    for line in file:
        columns = line.strip().split('\t') 
        protein_seq_dict[columns[0]] = [columns[1]]

for protein_id, protein_seq in protein_seq_dict.items():
    print(f"ProteinID: {protein_id}, ProteinSeq: {protein_seq}")
# print all entries in the same order as they appear in the file

#%% b) Only print peptides containing Tryptophan (W)
protein_seq_dict = {}

with open("proteins.tsv", "r") as file:
    next(file) # Skip the header
    for line in file:
        columns = line.strip().split('\t') 
        if "W" in columns[1]:
            protein_seq_dict[columns[0]] = [columns[1]]

for protein_id, protein_seq in protein_seq_dict.items():
    print(f"ProteinID: {protein_id}, ProteinSeq: {protein_seq}")
#%% c) Only print peptides that DO NOT contain X
protein_seq_dict = {}

with open("proteins.tsv", "r") as file:
    next(file) # Skip the header
    for line in file:
        columns = line.strip().split('\t') 
        if "W" not in columns[1]:
            protein_seq_dict[columns[0]] = [columns[1]]

for protein_id, protein_seq in protein_seq_dict.items():
    print(f"ProteinID: {protein_id}, ProteinSeq: {protein_seq}")
    
#%% 2.3 Sets — Helper function
file_path = r"C:\Users\yukim\Desktop\Python\Data\Data\regions.fna"
seq_id_set = set() # We create an empty set to keep track of the all sample IDs we have in regions.fna
duplicates = []

with open(file_path, "r") as file:
    for line in file:
        if line.startswith(">"):
            seq_id = line.strip()[1:].split()[0] # Extract the ID without the traling >
            if seq_id in seq_id_set:
                duplicates.append(seq_id)
            else:
                seq_id_set.add(seq_id)

if duplicates:
    print("Duplicate sequence IDs found:")
    for duplicate in duplicates:
        print(duplicate)
else:
    print("All sequence IDs are unique.")

#%% Task 1: Compare IDs between reads_ids.txt and reads.fna
# Author: Zimeng Liu
# Description: Check how many sequence IDs from reads_ids.txt occur in reads.fna,
# and compare runtime using list vs set lookups.

import time

# --- File paths ---
ids_file = r"C:\Users\yukim\Desktop\Python\Data\reads_ids.txt"
fasta_file = r"C:\Users\yukim\Desktop\Python\Data\reads.fna"

# --- Read IDs from text file ---
with open(ids_file) as f:
    query_ids = [line.strip() for line in f if line.strip()]

# --- Read IDs from FASTA file ---
with open(fasta_file) as f:
    fasta_ids = [line[1:].split()[0] for line in f if line.startswith(">")]

# --- Convert fasta_ids to set for faster lookup ---
fasta_ids_set = set(fasta_ids)

# --- 1️⃣ Using list (slow) ---
start = time.time()
found_list = [id_ for id_ in query_ids if id_ in fasta_ids]
end = time.time()
print(f"List lookup: found {len(found_list)} matches, time = {end - start:.5f} s")

# --- 2️⃣ Using set (fast) ---
start = time.time()
found_set = [id_ for id_ in query_ids if id_ in fasta_ids_set]
end = time.time()
print(f"Set lookup:  found {len(found_set)} matches, time = {end - start:.5f} s")

#%% Task 2: Compare IDs across three FASTA files
# Author: Zimeng Liu
# Description: Find common and missing IDs across regions_sub*.fna files.

# --- File paths ---
f1 = r"C:\Users\yukim\Desktop\Python\Data\regions_sub1.fna"
f2 = r"C:\Users\yukim\Desktop\Python\Data\regions_sub2.fna"
f3 = r"C:\Users\yukim\Desktop\Python\Data\regions_sub3.fna"

# --- Helper function to read fasta IDs ---
def read_fasta_ids(path):
    with open(path) as f:
        return {line[1:].split()[0] for line in f if line.startswith(">")}

ids1 = read_fasta_ids(f1)
ids2 = read_fasta_ids(f2)
ids3 = read_fasta_ids(f3)

# --- IDs present in both sub1 and sub2 ---
common_12 = ids1 & ids2
print(f"IDs in both sub1 and sub2: {len(common_12)}")

# --- IDs missing in sub3 ---
missing_in_3 = common_12 - ids3
print(f"IDs present in sub1&2 but NOT in sub3: {len(missing_in_3)}")
