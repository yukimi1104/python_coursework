# -*- coding: utf-8 -*-
"""
Title: Running Exercise I
Date: 2025-10-09
Author: Yiran Chen

Description:
    RunningExercise I — Hunting malaria genes.
    Task: Merge protein descriptions from BLASTX into FASTA file.
    1.Open and read malaria.fna 
    2.Open and read malaria.blastx.tab, extract protein description
    3.Output only entries with a non-null BLASTX hit
    4.Meerge protein descriptions to the head line of the FASTA file
Usage:
    python malaria.py malaria.fna malaria.blastx.tab output.txt

Required inputs:
    1.fasta_in     With tab-delimited headline and start with '>'
    2.blastx_tab   Tab-delimited table
Output:
    1.output.txt Text file with FASTA headers added protein descriptions.
                 Only non-null hits are written in.
"""

#%% Import the sys and os module.
import sys
import os

#%% Read and handle command-line arguments
if len(sys.argv)!= 4:
    print("Usage: python malaria.py fasta_in blast_tab output_file")
    sys.exit()

fasta_in = sys.argv[1]
blast_tab = sys.argv[2]
output_file = sys.argv[3]

#%% Check file existence using os
if not os.path.exists(fasta_in):
    print("Error: FASTA file not found:", fasta_in)
    sys.exit(1)
if not os.path.exists(blast_tab):
    print("Error: BLASTX file not found:", blast_tab)
    sys.exit(1)

#%% Read BLASTX file and make a blastx dictionary with key,value as gene_id and protein description.
blastx_dict = {}
with open(blast_tab, "r") as file:
    for line in file:
        line = line.strip()
        if line:
            columns = line.split("\t")
            gene_id = columns[0].strip()
            protein_description = columns[-1].strip()
        else:
            continue
 # If there is no protein description,do not add to blastx dictionary.
        if protein_description=="" or protein_description.upper()=="NULL":
            continue
        else:
            blastx_dict[gene_id] = protein_description
            

#%% Merge protein description in blastx with FASTA file
with open(output_file,"w") as out:
    with open(fasta_in, "r") as fasta:
        headline=""
        seq=[]
        for line in fasta:
            next(fasta)
            line = line.rstrip("\n")  #remove the '\n' in each line end
            if line.startswith(">"): #if it is the headline of a sequence
                if headline:
                    gene_id = headline.split("\t")[0].replace(">", "").strip() 
                    if gene_id in blastx_dict: #if gene_id can match keys in the blastx
                        new_headline = headline + "\tprotein=" + blastx_dict[gene_id]
                        out.write(new_headline + "\n")
                        out.write("\n".join(seq) + "\n")
                headline = line #add headline continuously
                seq = [] 
            else: #if it is not headline but the protein sequences
                seq.append(line)
        if headline: #because the first line in fasta does not output in the first loop, so last line should be added manually
            gene_id = headline.split("\t")[0].replace(">", "").strip()
            if gene_id in blastx_dict:
                new_headline = headline + "\tprotein=" + blastx_dict[gene_id]
                out.write(new_headline + "\n")
                out.write("\n".join(seq) + "\n")

print("Output file is finished:", output_file)
