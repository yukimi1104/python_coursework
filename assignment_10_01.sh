#Section 1
#Task 1: Determine your current working directory to confirm you are in the bio_project folder before processing any data; this prevents accidental overwrites in system directories and is essential for reproducible workflows in shared HPC systems where paths must be absolute or relative correctly.
pwd
#Task 2:List all files and directories in the raw/ folder with detailed information including permissions, sizes in human-readable format, and timestamps, to inspect data before analysis and ensure no hidden files (like .nextflow configs) are overlooked in bioinformatics tool setups.
#Task 3:Change your current directory to the raw/ folder, print the new location to verify, and then return to the previous directory, demonstrating safe navigation that avoids getting lost in deep HPC file trees during multi-step analyses like QC and alignment.
cd bio_project/raw/
pwd
ls -alh
cd ..
#Task 4:Count the number of hidden files (starting with '.') in your home directory, as bioinformatics tools often use hidden configs like .conda or .nextflow for reproducibility, and knowing how to reveal them helps in troubleshooting environment issues.
ls -alh|grep '^'|wc -l
#Task 5:Print your username and group memberships to check privileges, which is critical in shared HPC clusters where group permissions determine access to biobanks or cloud-mounted storage for large-scale genomic studies.
whoami
groups
id 
#Task 6:Measure the total disk space used by the raw/ directory in human-readable format, to assess storage requirements for scaling to larger datasets like multi-omics biobanks, ensuring you don't exceed quotas in HPC or cloud environments.
cd raw/
du -sh
#Task 7: Print available RAM and number of CPU cores to evaluate system resources before running memory-intensive tasks like alignment with BWA or variant calling, preventing job failures in HPC schedulers like Slurm.
free -h
lscpu
nproc
#Task 8:Use relative paths to navigate from the bio_project folder to a new temp/ folder one level up (creating it if needed), print the path to verify, then return, to practice flexible navigation for scripting in varying directory structures typical in cloud workflows.
cd
mkdir -p temp
cd ~/temp/
pwd
cd ..
rmdir temp
#Task 9:Visualize the structure of the bio_project directory tree up to depth 2, to quickly inspect organization for reproducibility, assuming tree is installed or falling back to ls if not (useful for auditing workflows before submission to journals or compliance).
cd ~/bio_project/
pwd
tree -L 2
#Task 10:Check free disk space on the current filesystem, extracting only the available space for the root mount, to monitor storage during large data transfers like syncing biobanks with rsync, preventing out-of-space errors in pipelines.
df -h|awk 'NR==2{print $4}'
#Section 2
#Task 1:Create subdirectories raw/, results/, scripts/, and logs/ inside bio_project if they don't exist, to structure your project for reproducible bioinformatics pipelines where raw data is separated from processed results and scripts.
#Task 2:Copy the file raw/ERR769583.fastq.gz to the results/ directory without overwriting existing files, verifying the operation with verbose output, to simulate backing up raw data before processing in a workflow.
pwd
cd /home/yukim/binp16/10-01/bio_project/raw
cp -vn ERR769583.fastq.gz /home/yukim/binp16/10-01/bio_project/results/
#Task 3:Rename the file raw/ERR769587.fastq.gz to raw/sample2.fastq.gz interactively to avoid overwrites, then confirm the new name with ls, to practice safe file management in analyses where sample IDs need standardization.
mv -i /home/yukim/binp16/10-01/bio_project/raw/ERR769587.fastq.gz /home/yukim/binp16/10-01/bio_project/raw/sample2.fastq.gz
#Task 4: Safely remove a temporary file (e.g., create temp.txt first if needed), prompting for confirmation, to demonstrate cautious deletion in HPC where rm -r could destroy critical datasets if misused.
echo "temporary content" > temp.txt
ls -lh temp.txt
rm -i temp.txt
#Task 5:Preview the first 8 lines (2 full reads) of raw/ERR769583.fastq.gz without decompressing to disk, to check read headers and quality before full processing in a sequencing QC step.
zcat sample2.fastq.gz|head -n 8
#Task 6:Synchronize the raw/ directory to a backup/ directory, preserving permissions and timestamps, with progress display, to model data transfers for biobanks or cloud integration in large-scale genomics.
mkdir -p backup/raw
rsync -avh --progress raw/ backup
#Task 7:Count the number of reads in raw/ERR769583.fastq.gz by calculating lines/4, to perform a sanity check on sequencing depth before alignment, ensuring the file is complete and not truncated.
zcat sample2.fastq.gz|wc -l|awk '{print $1/4}'
#Task 8:Scroll through the contents of raw/ERR769583.fastq.gz without decompressing to disk, searching for the first 'N' base to inspect for ambiguous sequences, useful for quality assessment in genomic analyses.
zgrep -n "N" sample2.fastq.gz | head
#Task 9:Monitor the last lines of a log file (create logs/pipeline.log with echo if needed) in real-time, to track progress of a running pipeline like FastQC or alignment, essential for long HPC jobs.
mkdir -p logs
echo "[$(date '+%F%T')]pipeline started">logs/pipeline.log
head logs/pipeline.log #'' all of the content will not be explained,$date means regarding the output of date as character
tail -n 50 -f logs/pipeline.log
tail -f logs/pipeline.log | grep --line-buffered -E 'ERROR|WARN'
#some_tools args... 2>&1|tee -a logs/pipeline.log
#some_tools args... >>logs/pipeline.log 2>&1 &
#Task 10:Create a file data.txt with sequence "ATGC", copy it to copy.txt, count its lines, and remove the copy interactively, to practice a full file management cycle in a safe, reversible way for learning.
echo "ATGC">data.txt
cp -v data.txt copy.txt
grep data.txt|wc -l
rm -i copy.txt
#Section 3
#Task 1:Redirect the first 8 lines of raw/ERR769583.fastq.gz to preview.txt while logging any errors to errors.log, to separate results from diagnostics in a QC step, ensuring clean outputs for reproducibility.
cd /home/yukim/binp16/10-01/bio_project/raw/
zcat sample2.fastq.gz 2>errors.log |head -n 8 >preview.txt
cat preview.txt
#Task 2:Pipe the output of zcat raw/ERR769583.fastq.gz to head and then count the lines, to demonstrate data flow without disk writes, useful for quick sanity checks on large FASTQ files in pipelines.
zcat sample2.fastq.gz|head|wc -l
#Task 3:Search for 'chr1' lines in raw/sample.vcf, counting the matches, to filter variants by chromosome in genomic studies, providing a quick summary without loading the full file.
grep 'chr1' sample.vcf|wc -l
#Task 4:Find all .fastq.gz files in the raw/ directory recursively and list them with details, to locate sequencing data in nested folders, common in multi-sample projects.
find -type f -name '*.fastq.gz' -exec ls -lh {} +
##+ → run the command once with as many files as possible at once. {} place holder
#Task 5:Display the top processes by CPU usage in batch mode for one iteration, filtering for any zcat processes, to monitor resource usage during data decompression in HPC.
top -b -n1 -o%CPU|awk 'NR<=15||/zcat/i'
#Task 6:Run zcat on raw/ERR769583.fastq.gz in the background, redirecting output to /dev/null and errors to logs/decomp.log, to simulate non-blocking decompression while preparing other steps in a pipeline.
zcat raw/ERR769583.fastq.gz > /dev/null 2> logs/decomp.log &
#Task 7:Identify and force-kill any running zcat processes matching the pattern, or report if none are running, to clean up stuck jobs in shared systems without wasting resources.
pgrep -af zcat
pkill -9 -f zcat || echo "No zcat processes found."
#Task 8:Combine stdout and stderr when attempting to list a non-existent file, saving to out.log, then preview the log, to demonstrate stream management for debugging tool errors in workflows.
ls non_existent.txt > out.log 2>&1 ||true; cat out.log
#Task 9:Sort the lines of raw/sample.vcf using input redirection from the file, saving the sorted output to sorted.vcf, to prepare data for tools that require sorted input like bedtools.
{ grep '^#'<sample.vcf; grep -v '^#' <sample.vcf| sort -t $'\t' -k1,1V -k2,2n; } > sorted.vcf
#Task 10:Create a multi-line BED file inline using a here document, including a header, save to temp.bed, make it executable if needed, and preview, to generate config files for genomic interval operations.
cat > temp.bed <<'EOF'
# chrom  start   end     name            score   strand
chr1     1000    1500    promoter_A      0       +
chr1     2000    2600    enhancer_B      0       -
chr2     300     900     peak_C          0       +
chr3     5000    5600    exon_D          0       -
EOF
chmod +x temp.bed  
echo "---- head temp.bed ----"
head -n 10 temp.bed
echo "---- columnized view ----"
column -t temp.bed | head
echo "---- line count ----"
wc -l temp.bed
#Section 4
#Task 1:Search for lines containing 'PASS' in raw/sample.vcf, counting the matches case-insensitively, to filter high-quality variants in genomic variant calling workflows.
grep -i 'PASS' sample.vcf|wc -l
#Task 2: Extract the first two columns (CHROM and POS) from raw/sample.vcf, skipping the header line, to summarize variant locations for downstream analysis like plotting.
awk '!/^#/ {print $1, $2}' sample.vcf > variants.txt
#Task 3:Sort the lines of raw/sample.vcf numerically by the second column (POS) in descending order, skipping the header, to rank variants by position for priority review.
awk '!/^#/' sample.vcf | sort -t $'\t' -k2,2nr --stable > variants_sorted.vcf
#Task 4:Extract the first column (CHROM) from raw/sample.vcf, sort it, and count unique entries with frequencies, ranking by count, to analyze variant distribution across chromosomes.
awk '!/^#/' sample.vcf \
| cut -f1 \
| sort \
| uniq -c \
| sort -k1,1nr -k2,2 \
> chrom_counts.txt
#Task 5: Filter lines from raw/sample.vcf where the second column (POS) is greater than 100, skipping the header, to select variants in a specific genomic region
awk '!/^#/ && $2 > 100' sample.vcf > pos_gt100.vcf
#Task 6:Remove the 'chr' prefix from the first column in raw/regions.bed, saving to a backup of the original, and preview the changes, to normalize chromosome names for tool compatibility.
cp regions.bed regions.bed.bak
sed -E 's/^chr//' regions.bed.bak > regions.bed
head regions.bed
#Task 7: Extract sequences from raw/4KRP_chainA.fasta (skipping headers), break into individual amino acids, sort and count unique with frequencies ranked, to compute amino acid composition in protein analysis.
grep -v '^>' 4KRP_chainA.fasta \
| tr -d '\n' \
| tr 'a-z' 'A-Z' \
| tr -cd 'A-Z' \
| fold -w1 \
| sort \
| uniq -c \
| sort -k1,1nr > aa_counts.txt
#Task 8:Compute the frequency of each amino acid in the sequences of raw/4KRP_chainA.fasta (skipping headers), printing sorted by count, to assess protein composition.
cat aa_counts.txt
awk '{
  count[$2]=$1; total+=$1
} END {
  printf("%-3s %10s %10s\n","AA","Count","Freq(%)");
  for (aa in count) {
    printf("%-3s %10d %9.2f\n", aa, count[aa], 100*count[aa]/total);
  }
}' aa_counts.txt \
| sort -k2,2nr > aa_composition.txt
#Task 9:Task**: In `raw/4KRP_chainB.fasta`, count the N-glycosylation motif **`N[^P][ST][^P]`** (as defined in Uniprot), allowing matches across line breaks, and also report **1-based start positions**.
awk '
/^>/ { next }
{ seq = seq toupper($0) }
END {
    cnt = 0
    n = length(seq)
    for (i = 1; i <= n - 3; i++) {
        a = substr(seq, i, 1)
        b = substr(seq, i + 1, 1)
        c = substr(seq, i + 2, 1)
        d = substr(seq, i + 3, 1)
        if (a == "N" && b != "P" && (c == "S" || c == "T") && d != "P") {
            cnt++
            printf("Count: %d\t1-based position: %d\n", cnt, i)
        }
    }
}'  4KRP_chainB.fasta
#Task 10: Replace all 'A' residues with 'N' in the sequence lines of raw/4KRP_chainA.fasta (leaving headers intact), saving to masked.fasta, to mask specific residues for privacy or testing in annotations.
sed '/^>/! s/A/N/g' 4KRP_chainA.fasta > masked.fasta
#g means substitution of all, not the first one
#Section 5
#Task 1: Update the package list and install the 'tree' utility using apt-get, assuming sudo access on a Debian-based system like Ubuntu, to enable directory visualization for project organization without needing advanced managers.
sudo apt-get update
sudo apt-get install -y tree
tree --version
#Task 2: Install the 'htop' process viewer using apt, to monitor system resources like CPU and memory during bioinformatics tasks, confirming installation by running its version.
sudo apt update
sudo apt install -y htop
htop --version
#Task 3:Install Python 3.11 using apt-get (adds PPA if needed on older systems), to set up a specific version for compatibility with legacy bioinformatics scripts, verifying the installation.
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
#sudo apt-get install -y software-properties-common
#sudo add-apt-repository ppa:deadsnakes/ppa -y
#sudo apt-get update
#sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
python3.11 --version
#Task 4：Install Python 3.12 using apt, to use a stable version for general data processing, then check the version to confirm.
# 1. Update your package list
sudo apt update
# 2. (Optional) Add Deadsnakes PPA if Python 3.12 isn't in your default repositories
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
# 3. Install Python 3.12
sudo apt install -y python3.12
# 4. Confirm the installation
python3.12 --version
#Task 5:Install Python 3.13 using apt-get (adds PPA if needed), for accessing the latest features in scripts, verifying with version output.
# 1. Update package lists
sudo apt update
# 2. Install PPA tools if needed
sudo apt install -y software-properties-common
# 3. Add Deadsnakes PPA (which publishes newer Python versions)  
sudo add-apt-repository -y ppa:deadsnakes/ppa
# 4. Refresh package lists again
sudo apt update
# 5. Install Python 3.13
sudo apt install -y python3.13
# 6. Confirm installation
python3.13 --version
#Task 6: Create a virtual environment named 'env311' using Python 3.11, activate it, to isolate dependencies for numpy-based array operations in data analysis.
# 1. Ensure Python 3.11 and venv module are installed
sudo apt install -y python3.11 python3.11-venv
# 2. Create the virtual environment
python3.11 -m venv env311
# 3. Activate the environment
source env311/bin/activate
# 4. (Optional) Verify activation and Python version
python --version
which python
#Task 7:Create 'env312' with Python 3.12, activate, install xgboost for ML models on genomic data, then list installed packages.
# 1. Ensure Python 3.12 and venv are installed
sudo apt install -y python3.12 python3.12-venv
# 2. Create the virtual environment
python3.12 -m venv env312
# 3. Activate the environment
source env312/bin/activate
# 4. Upgrade pip (recommended)
pip install --upgrade pip
# 5. Install XGBoost for machine learning on genomic data
pip install xgboost
# 6. List installed packages to confirm
pip list
#Task 8:Create 'env313' with Python 3.13, activate, install pandas for data frames in variant tables, deactivate after listing packages.
# 1. Make sure Python 3.13 and venv module are available
sudo apt install -y python3.13 python3.13-venv
# 2. Create the virtual environment
python3.13 -m venv env313
# 3. Activate the environment
source env313/bin/activate
# 4. Upgrade pip (optional but recommended)
pip install --upgrade pip
# 5. Install pandas for DataFrame handling (e.g. variant tables)
pip install pandas
# 6. List installed packages to confirm
pip list
# 7. Deactivate the environment after verifying
deactivate
#Task 9:Activate 'env311', install numpy for numerical computations, list all packages to confirm, then deactivate, to manage isolated environments for array-based bio data processing.
# 1. Activate the Python 3.11 environment
source env311/bin/activate
# 2. Install NumPy for numerical and array-based computations
pip install numpy
# 3. List all installed packages to confirm NumPy is included
pip list
# 4. Deactivate the environment after verification
deactivate
#Task 10: Switch between env312 and env313: activate env312, list packages, deactivate, then activate env313, list, to practice environment switching for different package needs in workflows.
# --- Step 1: Activate env312 ---
source env312/bin/activate
# --- Step 2: List packages in env312 (should include xgboost) ---
pip list
# --- Step 3: Deactivate env312 ---
deactivate
# --- Step 4: Activate env313 ---
source env313/bin/activate
# --- Step 5: List packages in env313 (should include pandas) ---
pip list
# --- Step 6: Deactivate env313 when done ---
deactivate
#Section 6:
#Task 1:Copy raw/ERR769583.fastq.gz to temp.fastq, compress it with gzip keeping the original, and list the results, to practice compression for storage efficiency in data archives.
# 1. Copy the FASTQ file to a new temporary file
cp sample2.fastq.gz temp.fastq.gz
# 2. Decompress it (so we have an uncompressed FASTQ for practice)
gunzip -c sample2.fastq.gz > temp.fastq
#gunzip -c means output standardly to screen, not cover the original file.so sample2.fastq.gz is not changes, the temp.fastq is decompressed.
# 3. Compress the new temp.fastq while keeping the original
gzip -k temp.fastq
#-k: keep the original
# 4. List the results to verify
ls -lh temp.fastq*
#Task 2:Archive the raw/ directory into raw.tgz with compression and verbose output, then check the archive size, to bundle data for sharing or backup in collaborative studies.
# 1. Create a compressed archive of the raw/ directory with verbose output
tar -czvf raw.tgz raw/
#tar → the archiving tool (short for “tape archive”).
#-c → create a new archive.
#-z → compress using gzip.
#-v → verbose mode, shows each file being added.
#-f raw.tgz → specifies the output file name.
#raw/ → the directory being archived.
# 2. List the resulting archive to check its size and existence
ls -lh raw.tgz
#Task 3:Measure disk usage for each file in raw/, sorting by size, to identify large datasets and manage storage in resource-limited environments.
du -h raw/* 2>/dev/null | sort -h
#du： the occupied actual size of disk.
#Task 4: Download ERR769583.fastq.gz to raw/ with resume support if interrupted, to handle unstable connections common in large data fetches from ENA.
curl -C - -L \
  -o raw/ERR769583.fastq.gz \
  https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR769/ERR769583/ERR769583.fastq.gz
ls -lh raw/ERR769583.fastq.gz
gzip -t raw/ERR769583.fastq.gz && echo "✅ GZIP OK" || echo "❌ GZIP FAIL"
echo "5e0f3b6ec51e9019cbb890c95e98fcd5  raw/ERR769583.fastq.gz" | md5sum -c -
# curl -C Continue / resume download;-L Follow redirects;-o output file path and name
#-t test. if file is destroyed
#Task 5:Fetch a JSON response from Ensembl API for ping, parsing with jq if available, to test API integration for annotation in scripts.
URL='https://rest.ensembl.org/info/ping'
curl -fsSL -H 'Accept: application/json' "$URL" \
| { command -v jq >/dev/null 2>&1 && jq || python3 -m json.tool 2>/dev/null || cat; }
#Quietly download JSON data from $URL, following redirects, and fail gracefully if the request doesn’t work.
#command -v jq checks if the jq command exists.&& jq means “if jq exists, run jq”.
#python3 -m json.tool is Python’s built-in JSON pretty-printer.2>/dev/null hides any errors.If Python is available, this prettifies the JSON too.If neither jq nor Python is available, just print the raw JSON as plain text.
#Task 6:Export the PATH variable after appending a bin/ directory, saving to path.log, to debug environment setups in tool integrations.
export PATH="$PATH:$(pwd)/bin" && echo "$PATH" > path.log
#Task 7:Search command history for 'zcat' uses, showing the last 5, to recall previous commands for building repeatable scripts (note: Bash must be interactive for history to show entries; test in interactive terminal).
history | grep zcat | tail -n 5
#Task 8:Determine the file type of all .gz files in raw/, to confirm compression and format before processing.
file raw/*.gz
#Task 9:Clear the terminal screen and reprint the current path, to reset focus during long sessions without losing orientation.
clear && pwd
#Task 10:Download a FASTQ, inspect its type and size, compress if needed, and archive to tgz, confirming each step, to practice a full data ingestion workflow.
#mkdir -p raw && cd raw
curl -I https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR164/ERR164407/ERR164407.fastq.gz #-I see head request
curl -L --range 0-1023 -o test.bin https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR164/ERR164407/ERR164407.fastq.gz
file test.bin
rm test.bin #--range 0-1023 downloads just the first 1024 bytes.-L follows redirects.file test.bin inspects those bytes to confirm it looks like a gzip.
curl -L -C - -O https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR164/ERR164407/ERR164407.fastq.gz
file ERR164407.fastq.gz
ls -lh ERR164407.fastq.gz  #-L follow redirects; -C - resume if interrupted; -O keep original filename.
gzip -t ERR164407.fastq.gz && echo "✅ GZIP OK" || echo "❌ GZIP FAIL"
cd ..
tar -cvzf raw.tgz raw/ #-c create, -v verbose (list files), -z gzip-compress the tar stream, -f raw.tgz output file name.
ls -lh raw.tgz
tar -tzf raw.tgz -t list, -z gunzip, -f file. without decompressing confirming paths like raw/ERR164407.fastq.gz are included.
#Section 7
#Task 1:Search for the pattern 'ATC' in raw/4KRP_chainA.fasta, counting occurrences, to find specific motifs in protein sequences for functional analysis.
grep -v '^>' 4KRP_chainA.fasta | tr -d '\n' | grep -oi 'ATC' | wc -l
grep -v '^>' 4KRP_chainA.fasta | tr -d '\n' | grep -oPi '(?=ATC)' | wc -l
awk 'BEGIN{IGNORECASE=1} /^>/{next} {seq=seq $0}
     END{for(i=1;i<=length(seq)-2;i++) if(toupper(substr(seq,i,3))=="ATC") {printf i (c++?",": "\n")}}' 4KRP_chainA.fasta
#Task 2:Match and count lines starting with '>' in raw/4KRP_chainA.fasta, to determine the number of sequences in a FASTA file for multi-entry processing.
grep -c '^>' 4KRP_chainA.fasta
#Task 3:Find and count sequences with 10 or more consecutive 'A's in raw/4KRP_chainA.fasta, to detect poly-A regions in proteins.
awk 'BEGIN{IGNORECASE=1}
  /^>/{
    if (seq ~ /A{10,}/) hit++
    seq=""
    next
  }
  {gsub(/[ \t\r]/,""); seq=seq $0}
  END{ if (seq ~ /A{10,}/) hit++; print hit+0 }' 4KRP_chainA.fasta
awk 'BEGIN{IGNORECASE=1}
  /^>/{
    if (NR>1 && s ~ /A{10,}/) print hdr
    hdr=$0; s=""; next
  }
  {gsub(/[ \t\r]/,""); s=s $0}
  END{ if (s ~ /A{10,}/) print hdr }' 4KRP_chainA.fasta
awk 'BEGIN{IGNORECASE=1}
/^>/{ if (seq!="") {
        tmp=seq; while (match(tmp,/A{10,}/)) { total++; printf("%s\tstart=%d\tlen=%d\n", id, off+RSTART, RLENGTH); off+=RSTART; tmp=substr(tmp,RSTART+1) }
      }
      id=$0; seq=""; off=0; next
    }
    {gsub(/[ \t\r]/,""); seq=seq toupper($0)}
END {
  if (seq!="") { tmp=seq; while (match(tmp,/A{10,}/)) { total++; printf("%s\tstart=%d\tlen=%d\n", id, off+RSTART, RLENGTH); off+=RSTART; tmp=substr(tmp,RSTART+1) } }
  printf("TOTAL_matches=%d\n", total+0)
}' 4KRP_chainA.fasta
#Task 4:Store a filename in a variable and echo it with its size, quoting to handle spaces, to practice safe variable expansion in scripts.
# Store filename (quotes protect spaces)
filename="4KRP_chainA.fasta"
# Echo the name and its size safely
echo "File: $filename"
echo "Size: $(stat -c%s "$filename") bytes"
#Task 5: Use brace expansion to create files sample1.txt and sample2.txt in one command, to batch generate placeholders for multi-sample analyses.
touch sample{1,2}.txt
ls sample*.txt
#Task 6:Match lines with 'chr1' or 'chr2' in raw/sample.vcf using alternation, extracting the CHROM column, to filter specific chromosomes. 
grep -E '^chr1|^chr2' sample.vcf | awk '{print $1}'
#Task 7: Simulate SSH key generation for bio@lab, with no passphrase, to set up secure remote access for HPC or cloud workflows.
ssh-keygen -t ed25519 -C "bio@lab" -N "" -f ~/.ssh/id_ed25519_biolab
cat ~/.ssh/id_ed25519_biolab.pub
ssh-copy-id -i ~/.ssh/id_ed25519_biolab.pub inf-30-2025@bioinf-serv2.cob.lu.se
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519_biolab ~/.ssh/config 2>/dev/null || true
chmod 644 ~/.ssh/id_ed25519_biolab.pub
#Task 8: Compute SHA256 checksum for raw/ERR769583.fastq.gz, save to check.sha, and verify it, to ensure data integrity after download.
sha256sum ERR769583.fastq.gz > check.sha
sha256sum -c check.sha
#Task 9:Use find to locate .fastq.gz files in raw/, pass null-safe to xargs for parallel line counting (limit to 2 processes), to batch process read counts politely on shared HPC (increase -P only if policy allows).
find -type f -name "*.fastq.gz" -print0 \
| xargs -0 -P 2 -n 1 zcat 2>/dev/null \
| grep -c '^@'
#Task 10:Create a simple SLURM-like script inline with here-doc, including a zcat command, make it executable, to orchestrate jobs in HPC.
# make a logs/ folder for SLURM outputs
mkdir -p logs
# write the job file via here-doc
mkdir -p logs

cat > job_zcat.slurm <<'SLURM'
#!/usr/bin/env bash
#SBATCH --job-name=zcat-demo
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --partition=short
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

set -euo pipefail

# optional: module system on clusters
module load gzip >/dev/null 2>&1 || true

IN="${1:-raw/ERR769583.fastq.gz}"

echo "==> File: $IN"
echo "==> Type: $(file -b "$IN" || true)"
echo "==> Counting reads (lines starting with @ in FASTQ)..."
READS=$(zcat "$IN" 2>/dev/null | grep -c '^@' || true)
echo "==> Read headers: $READS"
SLURM
chmod +x job_zcat.slurm
bash job_zcat.slurm ERR769583.fastq.gz | tee logs/zcat-demo_LOCAL.out
#sbatch job_zcat.slurm ERR769583.fastq.gz
#Section 8:
#Task 1:Create a mock VCF with echo if needed, then use awk to print the number of lines (variants), skipping the header, to count entries in variant files for summary stats.
cat > sample.vcf <<'VCF'
##fileformat=VCFv4.2
##source=mockGenerator
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
chr1    1001    rs1     A       G       99      PASS    .
chr1    1050    rs2     T       C       88      PASS    .
chr2    2003    rs3     G       A       76      PASS    .
chr2    2020    rs4     C       T       90      PASS    .
VCF
awk '!/^#/ {count++} END{print count+0}' sample.vcf
#Task 2:Use awk to extract the CHROM and POS columns from raw/sample.vcf, skipping the header, to generate a simple position list for genomic plotting.
awk '!/^#/ {print $1, $2}' sample.vcf > positions.txt
#Task 3: Filter raw/sample.vcf for QUAL > 20, printing the full lines, skipping header, to select high-quality variants for downstream analysis.
awk '!/^#/ && $6 > 20' sample.vcf
#Task 4: Compute the average QUAL from raw/sample.vcf, skipping header, to assess overall variant quality in a dataset.
awk '!/^#/ {sum += $6; n++} END {if (n>0) print "Average QUAL =", sum/n; else print "No variants found"}' sample.vcf
#Task 5:Print lines from raw/regions.bed where end - start > 20, to filter large intervals for genomic feature analysis.
awk '$3 - $2 > 20' regions.bed
awk '$3 - $2 > 20' regions.bed > regions_large.bed
awk '{len=$3 - $2; if(len > 20) print $0 "\t" len}' regions.bed > regions_large_withlen.bed
#Task 6:Create a mock FASTQ with echo if needed, then use awk to count reads with average quality >30 (Phred+33), to perform QC filtering.
cat > mock.fastq <<'FASTQ'
@r1
ACGTACGTAC
+
IIIIIIIIII
@r2
ACGTACGTAC
+
!!!!!!!!!!!!!!!!!!
@r3
ACGT
+
?@AB
FASTQ
awk '
BEGIN{
  # Printable ASCII from "!"(33) to "~"(126); index()-1 gives Phred score
  q="!\"#$%&'\''()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
}
NR%4==0{                         # quality line
  qual=$0; n=length(qual); s=0
  for(i=1;i<=n;i++){
    c=substr(qual,i,1)
    s += index(q,c)-1           # convert to Phred
  }
  if(n>0 && s/n>30) ok++
}
END{ print ok+0 }' mock.fastq
#Task 7:Use awk to add a new column to raw/sample.vcf (QUAL*2), printing the modified lines, skipping header, to normalize scores for comparison.
awk '!/^#/ { $6 = $6 * 2; print }' sample.vcf
#Task 8:Compute min, max, avg POS from raw/sample.vcf, skipping header, to get position stats for variant distribution.
awk '!/^#/ {
  pos = $2
  if (NR==1 || pos < min) min = pos
  if (NR==1 || pos > max) max = pos
  sum += pos; n++
}
END {
  if (n>0) printf "Min=%d\tMax=%d\tAverage=%.2f\n", min, max, sum/n
  else print "No variants found"
}' sample.vcf
#Task 9: Use awk to transpose columns in raw/regions.bed (mock tabular), to reformat for different tool inputs.
awk '
{
  for (i = 1; i <= NF; i++) {
    a[NR, i] = $i
  }
  if (NF > nf) nf = NF
}
END {
  for (i = 1; i <= nf; i++) {
    line = a[1, i]
    for (j = 2; j <= NR; j++) line = line "\t" a[j, i]
    print line
  }
}' regions.bed

#Task 10:
awk 'NR%4==2 {sum += length($0); n++} END {if (n>0) print "Average read length =", sum/n; else print "No reads found"}' mock.fastq
#Section 9
#Task 1:Normalize headers in raw/ERR1021663_1.fastq.gz by stripping the '/1' suffix from header lines (every 1st of 4 lines), previewing the first 20 lines to verify, to standardize read identifiers for compatibility with tools like aligners that expect clean headers without pair suffixes.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==1 {sub(/\/1$/, "", $0)} {print}' \
| head -n 20
#Task 2:Replace spaces with underscores in header lines of raw/ERR1021663_1.fastq.gz (every 1st of 4 lines), previewing the first 20 lines, to prevent parsing errors in downstream tools that treat spaces as delimiters in FASTQ headers.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==1 {gsub(/ /, "_")} {print}' \
| head -n 20
#Task 3:Extract only the sequence lines from raw/ERR1021663_1.fastq.gz (every 2nd of 4 lines), saving to a text file and previewing the first 20, to isolate sequences for analyses like motif searching without headers or qualities.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==2' \
| tee sequences.txt | head -n 20
#Task 4: Convert FASTQ to FASTA by changing '@' to '>' in headers (every 1st of 4 lines) and printing only headers and sequences (skipping '+' and quality), previewing the first 20 lines, to prepare data for tools that require FASTA input like BLAST.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==1 {sub(/^@/, ">"); print} NR%4==2 {print}' \
| tee sequences.fasta | head -n 20
#Task 5: Mask homopolymers of 6 or more 'A's in sequence lines of raw/ERR1021663_1.fastq.gz (every 2nd of 4 lines) with 'NNNNNN', keeping qualities intact and lengths preserved, to handle low-complexity regions that may cause alignment artifacts.
zcat ERR1021663_1.fastq.gz \
| awk '
  NR%4==2 {
    s=$0; out="";
    while (match(s, /[Aa]{6,}/)) {
      out = out substr(s,1,RSTART-1);
      rep=""; for (i=1;i<=RLENGTH;i++) rep=rep "N";   # preserve length
      out = out rep;
      s = substr(s, RSTART+RLENGTH);
    }
    $0 = out s;
  }
  { print }
' | head -n 20
zcat ERR1021663_1.fastq.gz \
| awk '
  NR%4==2 {
    s=$0; out="";
    while (match(s, /[Aa]{6,}/)) {
      out = out substr(s,1,RSTART-1);
      rep=""; for (i=1;i<=RLENGTH;i++) rep=rep "N";
      out = out rep;
      s = substr(s, RSTART+RLENGTH);
    }
    $0 = out s;
  }
  { print }
' | gzip > ERR1021663_1.masked.fastq.gz
#Task 6: Remove a known Illumina adapter sequence 'AGATCGGAAGAGC' from sequence lines in raw/ERR1021663_1.fastq.gz (every 2nd of 4 lines), previewing the first 40 lines case-insensitively, to perform basic adapter trimming before alignment, noting this is a simple global replacement not a full trimmer.
zcat ERR1021663_1.fastq.gz \
| awk 'BEGIN{IGNORECASE=1} NR%4==2{gsub(/AGATCGGAAGAGC/,"")} {print}' \
| head -n 40
#Task 7:Identify reads in raw/ERR1021663_1.fastq.gz where sequences (every 2nd of 4 lines) end with one or more 'N's, printing only their headers (every 1st of 4 lines), to flag ambiguous tail bases for quality filtering in sequencing pipelines.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==1 {hdr=$0} NR%4==2 && toupper($0) ~ /N+$/ {print hdr}'
#Task 8:Filter raw/ERR1021663_1.fastq.gz to keep only full 4-line reads where headers contain 'ERR1021663', to subset reads by sample ID in multi-sample FASTQ files for targeted analysis.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==1 {keep = ($0 ~ /ERR1021663/)} {if (keep) print}' \
| gzip > raw/ERR1021663_1.subset.fastq.gz
#Task 9：Append '/1' to headers in raw/ERR1021663_1.fastq.gz (every 1st of 4 lines) that do not already end with '/1' or '/2', previewing the first 16 lines, to standardize single-end reads for paired-end compatible tools.
zcat ERR1021663_1.fastq.gz \
| awk 'NR%4==1 {if ($0 !~ /\/[12]$/) $0=$0"/1"} {print}' \
| head -n 16
#Task 10:Mask repeats of 'AT' three or more times in sequence lines of raw/ERR1021663_1.fastq.gz (every 2nd of 4 lines) with 'NNNNNN', case-insensitively, to handle dinucleotide repeats that may affect variant calling accuracy.
zcat ERR1021663_1.fastq.gz \
| awk 'BEGIN{IGNORECASE=1} NR%4==2 {gsub(/(AT){3,}/, "NNNNNN")} {print}' \
| head -n 20









