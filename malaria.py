#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# ========== 参数检查 ==========
if len(sys.argv) != 4:
    print("Usage: python malaria.py fasta_in blast_tab output_file")
    sys.exit(1)

fasta_in = sys.argv[1]
blast_tab = sys.argv[2]
output_file = sys.argv[3]

# ========== 路径检查 ==========
if not os.path.exists(fasta_in):
    print("Error: FASTA file not found:", fasta_in)
    sys.exit(1)
if not os.path.exists(blast_tab):
    print("Error: BLASTX file not found:", blast_tab)
    sys.exit(1)

# ========== 构建 BLAST 结果字典 ==========
blastx_dict = {}
with open(blast_tab, "r", encoding="utf-8") as file:
    header = file.readline()  # 跳过表头
    for line in file:
        line = line.rstrip("\n")
        if not line:
            continue
        columns = line.split("\t")
        if len(columns) <= 9:
            continue
        gene_id = columns[0].strip()
        protein_description = columns[9].strip().rstrip(",; ")
        if protein_description == "" or protein_description.lower() == "null":
            continue
        if gene_id not in blastx_dict:  # 只保留首个匹配
            blastx_dict[gene_id] = protein_description

# ========== 读取 FASTA 并写出匹配的序列 ==========
written = 0

with open(fasta_in, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as out:
    
    header = None
    seq_lines = []
    
    for line in fin:
        line = line.rstrip("\n")
        if line.startswith(">"):
            # 如果前面有保存的序列，先处理它
            if header is not None:
                gene_id = header[1:].strip().split()[0]
                if gene_id in blastx_dict:
                    desc = blastx_dict[gene_id]
                    out.write(f"{header} protein={desc}\n")
                    out.write("".join(seq_lines) + "\n")
                    written += 1
            # 更新当前 header，清空序列缓存
            header = line
            seq_lines = []
        else:
            if line:  # 跳过空行
                seq_lines.append(line)
    
    # 最后一条也要处理
    if header is not None:
        gene_id = header[1:].strip().split()[0]
        if gene_id in blastx_dict:
            desc = blastx_dict[gene_id]
            out.write(f"{header} protein={desc}\n")
            out.write("".join(seq_lines) + "\n")
            written += 1

print(f"✅ Done. Wrote: {os.path.abspath(output_file)}  (matched sequences: {written})")


