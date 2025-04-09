"""
Module for generating abundance matrices from metagenomic data
"""
import os
import sys
import argparse
import pandas as pd
import subprocess
import tempfile
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def check_dependencies():
    """Check if required dependencies are installed"""
    dependencies = ['kraken2', 'bracken', 'ktImportText']
    missing = []
    
    for dep in dependencies:
        try:
            subprocess.run(['which', dep], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            missing.append(dep)
    
    if missing:
        logging.error(f"Missing dependencies: {', '.join(missing)}. Please install them or use the conda environment.")
        return False
    
    # Check for KRAKEN2_DB_DIR environment variable
    if 'KRAKEN2_DB_DIR' not in os.environ:
        logging.error("KRAKEN2_DB_DIR environment variable not set. Please set it to the path of your Kraken2 database.")
        return False
        
    return True

def run_command(cmd, log_file=None):
    """Run a shell command and optionally log the output"""
    logging.info(f"Running command: {cmd}")
    
    if log_file:
        with open(log_file, 'w') as f:
            process = subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
    else:
        process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    if process.returncode != 0:
        logging.error(f"Command failed with return code {process.returncode}")
        if not log_file and process.stdout:
            logging.error(process.stdout.decode('utf-8'))
    
    return process.returncode


def create_abundance_matrix(input_files, output_file):
    """
    Creates a relative abundance matrix from a list of Bracken files.

    Args:
        input_files (list): A list of paths to Bracken output files.
        output_file (str): The path to the output CSV file.
    """
    all_data = []
    sample_names = []

    for file_path in input_files:
        # Extract sample name
        sample_name = os.path.basename(file_path).replace("_species.bracken", "")
        sample_names.append(sample_name)

        # Read the Bracken file
        df = pd.read_csv(file_path, sep='\t')

        # Check for required columns and handle variations
        if 'fraction_total_reads' in df.columns:
            df_rel = df[['name', 'fraction_total_reads']].copy()
        elif 'new_est_frac_reads' in df.columns:
            df_rel = df[['name', 'new_est_frac_reads']].copy()
            df_rel.rename(columns={'new_est_frac_reads': 'fraction_total_reads'}, inplace=True)
        else:
            raise ValueError(f"Required columns not found in {file_path}")

        df_rel.rename(columns={'fraction_total_reads': sample_name}, inplace=True)
        all_data.append(df_rel)

    # Merge dataframes.
    merged_df = all_data[0]
    for df in all_data[1:]:
        merged_df = pd.merge(merged_df, df, on='name', how='outer')  # outer join

    merged_df.fillna(0, inplace=True)  # Replace NaN with 0
    merged_df.set_index('name', inplace=True)  # Set 'name' as index
    merged_df.to_csv(output_file)  # Save as CSV
    
    return output_file


def process_raw_data(raw_files, output_dir, threads=8):
    """
    Process raw fastq files through the taxonomic profiling pipeline
    
    Args:
        raw_files (list): List of raw fastq files
        output_dir (str): Output directory
        threads (int): Number of threads to use
    
    Returns:
        str: Path to the abundance matrix file
    """
    # Check dependencies first
    if not check_dependencies():
        logging.error("Missing required dependencies. Please install them before proceeding.")
        sys.exit(1)
    
    # Create necessary directories
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subdirectories
    preprocessed_dir = os.path.join(output_dir, "preprocessed")
    kraken2_dir = os.path.join(output_dir, "kraken2")
    bracken_dir = os.path.join(output_dir, "bracken")
    krona_dir = os.path.join(output_dir, "krona")
    logs_dir = os.path.join(output_dir, "logs")
    
    for directory in [preprocessed_dir, kraken2_dir, bracken_dir, krona_dir, logs_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # Get sample names from raw files
    samples = []
    for raw_file in raw_files:
        # Extract sample name from filename (assuming format like sample_R1.fastq.gz)
        base_name = os.path.basename(raw_file)
        sample_name = base_name.split('_')[0]
        if sample_name not in samples:
            samples.append(sample_name)
    
    logging.info(f"Found {len(samples)} samples: {', '.join(samples)}")
    
    # Process each sample
    bracken_files = []
    for sample in samples:
        # Create sample directories
        sample_kraken_dir = os.path.join(kraken2_dir, sample)
        sample_bracken_dir = os.path.join(bracken_dir, sample)
        sample_krona_dir = os.path.join(krona_dir, sample)
        
        for directory in [sample_kraken_dir, sample_bracken_dir, sample_krona_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Find R1 and R2 files for this sample
        r1_files = [f for f in raw_files if f"{sample}_" in f and "R1" in f]
        r2_files = [f for f in raw_files if f"{sample}_" in f and "R2" in f]
        
        if not r1_files or not r2_files:
            logging.warning(f"Could not find paired files for sample {sample}")
            continue
        
        # For simplicity, we'll just use the first pair if multiple are found
        r1_file = r1_files[0]
        r2_file = r2_files[0]
        
        logging.info(f"Processing sample {sample} with files:\n  R1: {r1_file}\n  R2: {r2_file}")
        
        # Run Kraken2
        kraken_report = os.path.join(sample_kraken_dir, f"{sample}.k2report")
        kraken_cmd = f"kraken2 --db $KRAKEN2_DB_DIR --threads {threads} --paired " \
                    f"--report {kraken_report} " \
                    f"--output /dev/null " \
                    f"{r1_file} {r2_file}"
        
        logging.info(f"Running Kraken2 for sample {sample}...")
        kraken_log = os.path.join(logs_dir, f"{sample}_kraken2.log")
        if run_command(kraken_cmd, kraken_log) != 0:
            logging.error(f"Kraken2 failed for sample {sample}. Check log at {kraken_log}")
            continue
        
        # Run Bracken
        bracken_species = os.path.join(sample_bracken_dir, f"{sample}_species.bracken")
        bracken_cmd = f"bracken -d $KRAKEN2_DB_DIR -i {kraken_report} " \
                     f"-o {bracken_species} -l S -r 150"
        
        logging.info(f"Running Bracken for sample {sample}...")
        bracken_log = os.path.join(logs_dir, f"{sample}_bracken.log")
        if run_command(bracken_cmd, bracken_log) != 0:
            logging.error(f"Bracken failed for sample {sample}. Check log at {bracken_log}")
            continue
        
        # Generate Krona plot
        krona_html = os.path.join(sample_krona_dir, f"{sample}_species.html")
        krona_temp = os.path.join(sample_krona_dir, f"{sample}_forKrona.txt")
        
        # Extract data for Krona
        try:
            df = pd.read_csv(bracken_species, sep='\t')
            # Filter for significant abundance (>= 0.01%)
            df = df[df['fraction_total_reads'] >= 0.0001]
            # Create Krona input file
            with open(krona_temp, 'w') as f:
                for _, row in df.iterrows():
                    f.write(f"{row['fraction_total_reads']*100}\t{row['name']}\n")
            
            # Generate Krona plot
            krona_cmd = f"ktImportText -o {krona_html} {krona_temp}"
            logging.info(f"Generating Krona plot for sample {sample}...")
            krona_log = os.path.join(logs_dir, f"{sample}_krona.log")
            run_command(krona_cmd, krona_log)
        except Exception as e:
            logging.error(f"Failed to generate Krona plot for sample {sample}: {e}")
        
        bracken_files.append(bracken_species)
    
    if not bracken_files:
        logging.error("No Bracken files were generated. Cannot create abundance matrix.")
        sys.exit(1)
    
    # Create abundance matrix
    abundance_matrix = os.path.join(output_dir, "abundance_matrix.csv")
    logging.info(f"Creating abundance matrix from {len(bracken_files)} Bracken files...")
    create_abundance_matrix(bracken_files, abundance_matrix)
    
    logging.info(f"Process complete. Abundance matrix saved to: {abundance_matrix}")
    return abundance_matrix
