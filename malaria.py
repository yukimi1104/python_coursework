#%% Import the sys and os module.
import sys
import os

#%% Read and handle command-line arguments
if len(sys.argv)!= 4:
    print("Usage: python malaria.py fasta_in blast_tab output_file")
    sys.exit()

fasta_in = sys.argv[1] #path to the input file(malaria.fna)
blast_tab = sys.argv[2] #path to malaria.blastx.tab
output_file = sys.argv[3] #the output path
#%% Check input files existence using os module
if not os.path.exists(fasta_in):
    print("Error: FASTA file not found:", fasta_in)
    sys.exit(1)
if not os.path.exists(blast_tab):
    print("Error: BLASTX file not found:", blast_tab)
    sys.exit(1)

#%% Read BLASTX file and make a blastx dictionary with key,value as gene_id and protein description.
blastx_dict = {} #make an empty dictionary of blastx results
with open(blast_tab, "r") as file:
    header=file.readline()  # read and skip header line
    for line in file:
        line = line.rstrip("\n") #delte '\n' at the end of each line
        if not line:
            continue #skip empty lines
        columns = line.split("\t")
        if len(columns) <= 9:
            continue   #skip the lines with out protein description column
        gene_id = columns[0].strip() #extract gene id
        protein_description = columns[9].strip().rstrip(",; ") #extrace column[9](protein description)
        # If there is no protein description, do not add to blastx dictionary and skip.
        if protein_description == "" or protein_description.lower() == "null":
            continue
        if gene_id not in blastx_dict:  #remove the not aligned proteins and only saving first hits
            blastx_dict[gene_id] = protein_description
            

#%% Merge protein description in blastx with FASTA file
written=0 #count the number of entries, start with 0
with open(output_file,"w") as out:
    with open(fasta_in, "r") as fasta:
        header_line="" #define empty headline and protein sequences
        seq=[]
        for line in fasta:
            line = line.rstrip("\n")  #remove the '\n' in each line end
            if line.startswith(">"): #if it is the headline of a sequence（in fasta files start with ">")
                if header_line:#if the headline of each id is not empty
                    gene_id = header_line.split("\t")[0].replace(">", "").strip() #remove ">" and spaces and get gene id
                    if gene_id in blastx_dict: #if gene_id can match keys in the blastx
                        new_header = header_line + "\tprotein=" + blastx_dict[gene_id] #join the protein description
                        out.write(new_header + "\n")
                        if seq:  #if the sequence of this gene id is not empty
                            out.write("\n".join(seq) + "\n")
                        else:
                            out.write("\n") #skip empty sequences
                        written += 1 #write in the entry hitted
                header_line = line #add headline continuously
                seq = [] 
            else: #if it is not headline but the protein sequences
                seq.append(line)
        if header_line: #because the first line in fasta does not output in the first loop, so last line should be added manually
             gene_id = header_line.split("\t")[0].replace(">", "").strip()
             if gene_id in blastx_dict:
                new_header = header_line + "\tprotein=" + blastx_dict[gene_id]
                out.write(new_header + "\n")
                if seq:
                    out.write("\n".join(seq) + "\n")
                else:
                    out.write("\n")
                written += 1

print(f"Output is done: {output_file}  (match {written} entries)")
