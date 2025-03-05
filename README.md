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


