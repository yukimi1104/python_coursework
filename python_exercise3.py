# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 17:37:07 2025

@author: yukim
"""

"""
Date: 2025-10-08
Author: Yiran Chen

Description:
    3. Program control and logic — solutions in Spyder-style cells.
    Includes: loops/conditions (6–13) and error exceptions (14–15).

Usage:
    Run cell-by-cell with Ctrl+Enter. All input() have safe fallbacks.
"""
#%% 3.1 Loops and conditions — 6
# Greeting: special for me, neutral for others

MY_NAME = "Yukim"  # <- change to your name if you like

def greet_once():
    try:
        name = input("What is your name: ").strip()
    except Exception:
        name = MY_NAME  # fallback
    if name == MY_NAME:
        print(f"So very nice to see you {name}!")
    else:
        print(f"Hi {name}")

greet_once()

#%% 3.1 Loops and conditions — 7
# Greeting: special for me, special-for-friends, neutral for others

MY_NAME = "Yukim"
FRIENDS = {"Afriend", "Bfriend", "Cfriend"}  # edit as you like

def greet_with_friends():
    try:
        name = input("What is your name: ").strip()
    except Exception:
        name = "Afriend"  # fallback
    if name == MY_NAME:
        print(f"So very nice to see you {name}!")
    elif name in FRIENDS:
        print(f"What's up {name}!")
    else:
        print(f"Hi {name}")

greet_with_friends()

#%% 3.1 Loops and conditions — 8
# FizzBuzz (single value)

def fizzbuzz_one():
    try:
        n = int(input("Provide the next number: "))
    except Exception:
        n = 15  # safe fallback
    if n % 15 == 0:
        print("fizzbuzz")
    elif n % 3 == 0:
        print("fizz")
    elif n % 5 == 0:
        print("buzz")
    else:
        print(n)

fizzbuzz_one()

#%% 3.1 Loops and conditions — 9
# Real FizzBuzz (1..100)

def fizzbuzz_all():
    for n in range(1, 101):
        if n % 15 == 0:
            print("fizzbuzz")
        elif n % 3 == 0:
            print("fizz")
        elif n % 5 == 0:
            print("buzz")
        else:
            print(n)

# Uncomment to run:
# fizzbuzz_all()

#%% 3.1 Loops and conditions — 10
# Golf scoring on 8 holes

PARS = [4, 3, 5, 2, 5, 4, 7, 6]  # holes 1..8

def golf_score():
    try:
        hole = int(input("Hole (1-8): "))
        strokes = int(input("Strokes: "))
    except Exception:
        hole, strokes = 4, 3  # fallback example
    par = PARS[hole - 1]
    diff = strokes - par
    if diff <= -3:
        name = "Albatross"
    elif diff == -2:
        name = "Eagle"
    elif diff == -1:
        name = "Birdie"
    elif diff == 0:
        name = "Par"
    elif diff == 1:
        name = "Boogie"
    else:
        name = "Double boogie"
    print(name)

golf_score()

#%% 3.1 Loops and conditions — 11
# enumerate: uppercase every second letter starting from the first

letter_list = ["a", "b", "c", "e", "f", "g", "h", "i"]

# Print one per line with requested transformation:
for idx, letter in enumerate(letter_list, start=1):
    if idx % 2 == 1:  # 1st, 3rd, 5th... -> uppercase
        print(letter.upper())
    else:
        print(letter)

#%% 3.1 Loops and conditions — 12 *
# mRNA: find positions (1..10) of Tyr codons (UAU, UAC)

mrna = "UAUAAACGAUACCAUUACUAUGACCAUGGG"
# split into 10 codons of length 3
codons = [mrna[i:i+3] for i in range(0, len(mrna), 3)]
TYR = {"UAU", "UAC"}
tyr_positions = [i for i, c in enumerate(codons, start=1) if c in TYR]
print("Tyr codon positions (1..10):", tyr_positions)

#%% 3.1 Loops and conditions — 13 *
# First 1000 prime numbers

def first_1000_primes():
    primes = [2]
    candidate = 3
    from math import isqrt
    while len(primes) < 1000:
        limit = isqrt(candidate)
        is_prime = True
        for p in primes:
            if p > limit:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 2  # skip even numbers
    return primes

# Uncomment to print them all:
# print("\n".join(map(str, first_1000_primes())))

#%% 3.2 Error exceptions — 14
# Ask user for DNA and RAISE an exception if any non-ACGT is present

def validate_dna_raises():
    try:
        seq = input("Please type a DNA sequence: ").strip()
    except Exception:
        seq = "GATCX"  # fallback shows the exception behavior
    for ch in seq.upper():
        if ch not in "ACGT":
            raise ValueError(f"Invalid nucleotide '{ch}' found in sequence.")
    print("Sequence is valid (ACGT only).")

# Uncomment to see the exception raised:
# validate_dna_raises()

#%% 3.2 Error exceptions — 15 *
# Prompt until all nucleotides valid; show messages accordingly

def prompt_until_valid_dna():
    while True:
        try:
            seq = input("Please type a DNA sequence: ").strip()
        except Exception:
            # fallback cycles through some examples
            for trial in ["ACCAB", "AGGTAHT", "GATC"]:
                print(trial)  # echo as if user typed it
                seq = trial
                # fall through to validation
                for ch in seq.upper():
                    if ch not in "ACGT":
                        print("Your sequence contains an invalid nucleotide. Please try again.")
                        break
                else:
                    print("You have entered a valid DNA sequence.")
                    return
            return  # end fallback
        # Validate user-provided seq
        for ch in seq.upper():
            if ch not in "ACGT":
                print("Your sequence contains an invalid nucleotide. Please try again.")
                break
        else:
            print("You have entered a valid DNA sequence.")
            return

# Uncomment to run interactively:
# prompt_until_valid_dna()
