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

# Define the alphabet
bases = "ATCG"

# Use a nested loop (or list comprehension) to build all 3-letter combinations
codons_from_alphabet = [a + b + c for a in bases for b in bases for c in bases]

# Check result
print("Number of codons generated:", len(codons_from_alphabet))  # should be 4*4*4 = 64
print("First 10 codons:", codons_from_alphabet[:10])

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
file_path = "proteins.tsv"
with open(file_path, "w", encoding="utf-8") as f:
    f.write("ProteinID\tProteinSeq\n")
    f.write("prot1\tAGSATGDASD\n")
    f.write("prot4\tASLWASLD\n")
    f.write("prot9\tPPASDSADSAD\n")
    f.write("prot2\tXXSWKJXS\n")
    f.write("prot8\tPSOASSADASD\n")

#%% a) Load the table into a dictionary
proteins = {}  # empty dictionary

# open the file and read line by line
with open(file_path, "r", encoding="utf-8") as f:
    header = f.readline()  # skip the first header line
    for line in f:
        if not line.strip():
            continue  # skip any blank lines
        pid, seq = line.strip().split("\t")
        proteins[pid] = seq

# print all entries in the same order as they appear in the file
print("All protein entries (file order):")
for pid in proteins:
    print(f"{pid}: {proteins[pid]}")

#%% b) Only print peptides containing Tryptophan (W)
print("\nProteins containing Tryptophan (W):")
for pid, seq in proteins.items():
    if "W" in seq:
        print(f"{pid}: {seq}")

#%% c) Only print peptides that DO NOT contain X
print("\nProteins without X:")
for pid, seq in proteins.items():
    if "X" not in seq:
        print(f"{pid}: {seq}")

#%% 2.3 Sets — Helper function
# Define a small helper function to read FASTA IDs (lines starting with ">")

def fasta_ids(filepath):
    """Return a list of all sequence IDs (first word after '>') from a FASTA file."""
    ids = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(">"):
                ids.append(line[1:].strip().split()[0])
    return ids

#%% 2.3 Sets — 1
# Create a small demo file (replace with your real file in actual use)
with open("regions.fna", "w", encoding="utf-8") as f:
    f.write(">r1\nATGCG\n>r2\nAAGTC\n>r3\nTTTGG\n>r2\nCCCAG\n")  # duplicate r2 for testing

# Get all IDs
ids_regions = fasta_ids("regions.fna")

# Check uniqueness
unique_ids = set(ids_regions)

if len(ids_regions) == len(unique_ids):
    print("✅ All sequence IDs are unique.")
else:
    print("❌ Some IDs are duplicated.")
    duplicates = [i for i in ids_regions if ids_regions.count(i) > 1]
    print("Duplicated IDs:", sorted(set(duplicates)))

#%% 2.3 Sets — 2
# Create demo files
with open("reads.fna", "w", encoding="utf-8") as f:
    f.write(">a\nAAA\n>b\nCCC\n>c\nGGG\n>d\nTTT\n")

with open("reads_ids.txt", "w", encoding="utf-8") as f:
    f.write("a\nx\nc\nb\nz\n")

# Read IDs
reads_ids = [line.strip() for line in open("reads_ids.txt", "r", encoding="utf-8") if line.strip()]
fasta_ids_list = fasta_ids("reads.fna")
fasta_ids_set = set(fasta_ids_list)

# Compare lookup speeds
import time

# Using list
t0 = time.perf_counter()
hits_list = sum(1 for rid in reads_ids if rid in fasta_ids_list)
t1 = time.perf_counter()

# Using set
t2 = time.perf_counter()
hits_set = sum(1 for rid in reads_ids if rid in fasta_ids_set)
t3 = time.perf_counter()

print(f"Hits using list : {hits_list}, time = {(t1 - t0) * 1e6:.1f} µs")
print(f"Hits using set  : {hits_set}, time = {(t3 - t2) * 1e6:.1f} µs")

#%% 2.3 Sets — 3
# Create demo files
with open("regions_sub1.fna", "w", encoding="utf-8") as f:
    f.write(">a\nNNN\n>b\nNNN\n>c\nNNN\n>d\nNNN\n")

with open("regions_sub2.fna", "w", encoding="utf-8") as f:
    f.write(">b\nNNN\n>c\nNNN\n>e\nNNN\n>f\nNNN\n")

with open("regions_sub3.fna", "w", encoding="utf-8") as f:
    f.write(">c\nNNN\n>g\nNNN\n")

# Load IDs as sets
ids1 = set(fasta_ids("regions_sub1.fna"))
ids2 = set(fasta_ids("regions_sub2.fna"))
ids3 = set(fasta_ids("regions_sub3.fna"))

# IDs common to sub1 and sub2
common_1_2 = ids1 & ids2  # intersection
# Among those, which are not in sub3
not_in_3 = common_1_2 - ids3  # set difference

print(f"IDs in both sub1 and sub2 ({len(common_1_2)}): {sorted(common_1_2)}")
print(f"IDs not in sub3 ({len(not_in_3)}): {sorted(not_in_3)}")
