import subprocess
import os
import glob
import pandas as pd
import sys

def run_quast_and_merge_results(input_dir, output_file):
    """
    Runs QUAST on all genome FASTA files in the given input directory
    and consolidates the results into a single output file.
    """
    # Search for FASTA files with different extensions (case-insensitive)
    fasta_files = glob.glob(os.path.join(input_dir, "*.fasta")) + \
                  glob.glob(os.path.join(input_dir, "*.fa")) + \
                  glob.glob(os.path.join(input_dir, "*.fna")) + \
                  glob.glob(os.path.join(input_dir, "*.FASTA")) + \
                  glob.glob(os.path.join(input_dir, "*.FA")) + \
                  glob.glob(os.path.join(input_dir, "*.FNA"))

    # Debugging: Print detected files
    print("Searching in: {}".format(input_dir))
    print("Detected FASTA files: {}".format(fasta_files))

    if not fasta_files:
        print("⚠️ No FASTA files found. Check your directory and file extensions.")
        sys.exit(1)

    all_results = []

    for fasta in fasta_files:
        base_name = os.path.basename(fasta).replace(".fasta", "").replace(".fa", "").replace(".fna", "")
        output_dir = os.path.join(os.path.dirname(output_file), "quast_{}".format(base_name))
        os.makedirs(output_dir, exist_ok=True)

        try:
            # QUAST command
            cmd = [
                "quast", fasta,
                "-o", output_dir,
                "--gene-finding"
            ]
            subprocess.run(cmd, check=True)
            print("✅ QUAST analysis completed for {}. Results saved in {}".format(fasta, output_dir))

            # Read the QUAST report file and extract relevant data
            report_path = os.path.join(output_dir, "report.tsv")
            if os.path.exists(report_path):
                df = pd.read_csv(report_path, sep='\t', index_col=0)
                df_transposed = df.T  # Transpose for better formatting
                df_transposed.insert(0, "Genome", base_name)
                all_results.append(df_transposed)

        except subprocess.CalledProcessError as e:
            print("❌ Error running QUAST on {}: {}".format(fasta, e))

    # Combine all results into a single file
    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        combined_df.to_csv(output_file, sep='\t', index=False)
        print("📄 All QUAST results merged and saved to {}".format(output_file))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python quast_combined_qc.py <input_directory> <output_file>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_results_file = sys.argv[2]

    # Validate input directory
    if not os.path.exists(input_directory):
        print("⚠️ Error: Input directory '{}' does not exist.".format(input_directory))
        sys.exit(1)

    run_quast_and_merge_results(input_directory, output_results_file)
