# Listeria_Project
1. Download Listeria monocytogenes genomic assemblies from NCBI using NCBI `datasets` tool
Install using curl
Linux
Download datasets: curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets'
Download dataformat: curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/dataformat'
Make them executable: chmod +x datasets dataformat

2. Download Assembly from NCBI and Data Preparation

```
./datasets  download genome accession --inputfile assm_accs.txt --include genome,cds,gff3
unzip ncbi_dataset.zip

# Define the destination folder
DEST_DIR="assembly"
# Loop through each folder and copy its contents

for folder in GCA_*; do
    if [ -d "$folder" ]; then
        cp "$folder"/* "$DEST_DIR"/
    fi
done

# Change file name

for file in GCA_*.fna; do 
    mv "$file" "$(echo "$file" | cut -d'_' -f1-2).fna"
done

```

3. Abricate-Virulence Gene Identifiaction
```
abricate --db vfdb *.fna > results.tsv
wc -l results.tsv

# Use cutoff thresholds to retain high-confidence virulence genes (e.g., identity > 90%, coverage > 90%).

cat results.tsv | awk -F"\t" '$10 > 90 && $11 > 90' > filtered_results.tsv
wc -l filtered_results.tsv

# Summarize results

abricate --summary filtered_results.tsv > summary.tsv
```
