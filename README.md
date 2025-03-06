# Listeria_Project
1. Download Listeria monocytogenes genomic assemblies from NCBI using NCBI `datasets` tool
Install using curl
Linux
Download datasets: curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets'
Download dataformat: curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/dataformat'
Make them executable: chmod +x datasets dataformat
2. Downloading

```
./datasets  download genome accession --inputfile assm_accs.txt --include genome,cds,gff3
unzip ncbi_dataset.zip
```

3. Parse files
```
#!/bin/bash

# Define the destination folder
DEST_DIR="assembly"
# Loop through each folder and copy its contents
for folder in GCA_*; do
    if [ -d "$folder" ]; then
        cp "$folder"/* "$DEST_DIR"/
    fi
done

echo "Files have been copied to $DEST_DIR."
```
