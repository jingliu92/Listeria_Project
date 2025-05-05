# Listeria_Project
1. Download Listeria monocytogenes genomic assemblies from NCBI using NCBI `datasets` tool
Install using curl
```
Download datasets: curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets'
Download dataformat: curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/dataformat'
Make them executable: chmod +x datasets dataformat
```

3. Download Assembly from NCBI and Data Preparation

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

# Add GCA to each sequence
```
for f in *.fna; do
    sample_id="${f%%.fna}"
    sed -i "s/^>/>${sample_id}_/" "$f"
done
```

3. Abricate-Virulence Gene Identifiaction
```
abricate --db vfdb *.fna > results.tsv
wc -l results.tsv

# Use cutoff thresholds to retain high-confidence virulence genes (e.g., identity > 90%, coverage > 90%).

head -n 1 results.tsv > filtered_results.tsv && awk -F"\t" '$10 > 90 && $11 > 90' results.tsv >> filtered_results.tsv

wc -l filtered_results.tsv

# Summarize results

abricate --summary filtered_results.tsv > summary.tsv
```

4. Prodigal Gene Functional Analysis
```
for genome in ./*.fna; do     sample_name=$(basename $genome.fna);
prokka --outdir ./prokka_anno/$sample_name --prefix $sample_name --kingdom Bacteria --genus Listeria --species monocytogenes --cpus 8 $genome; done
```
5. Pangenome Analysis with Roary
```
for folder in GCA_*; do
    if [ -d "$folder" ]; then  # Check if it is a directory
        gff_file=$(find "$folder" -type f -name "*.gff")  # Find the .gff file in the folder
        if [ -n "$gff_file" ]; then  # Check if a .gff file exists
            cp "$gff_file" all_gff_files/  # Copy .gff file to new folder
            echo "Copied: $gff_file"
        fi
    fi
done

for file in GCA_*.fna.fna.gff; do
    new_name=$(echo "$file" | sed 's/.fna.fna//')  # Remove the extra .fna.fna
    mv "$file" "$new_name"
    echo "Renamed: $file -> $new_name"
done

# Run Roary
roary -e -n -p 8 -v -f ./pangenome_output *.gff


1. sequence of lmo2821
2. cat all the fna file in to one single file

cat *.fna > all_combined.fasta

makeblastdb -in all_combined.fasta -dbtype nucl -out listeria_all_db

blastn -query lmo2821.fasta -db listeria_all_db -out lmo2821_clinical1.tsv \
-outfmt '6 qseqid sseqid pident length qlen slen qstart qend sstart send evalue bitscore'
```

# quast
```
quast.py *.fna -o quast_output

```
   
