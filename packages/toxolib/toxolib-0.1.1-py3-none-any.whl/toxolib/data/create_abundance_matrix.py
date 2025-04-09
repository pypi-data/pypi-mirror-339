#!/usr/bin/env python3
"""
Script to create abundance matrix from Bracken files
"""
import argparse
import pandas as pd
import os

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
            df_rel.rename(columns = {'new_est_frac_reads': 'fraction_total_reads'}, inplace=True)
        else:
            raise ValueError(f"Required columns not found in {file_path}")

        df_rel.rename(columns={'fraction_total_reads': sample_name}, inplace=True)
        all_data.append(df_rel)

    # Merge dataframes.
    merged_df = all_data[0]
    for df in all_data[1:]:
        merged_df = pd.merge(merged_df, df, on='name', how='outer') # outer join

    merged_df.fillna(0, inplace=True)  # Replace NaN with 0
    merged_df.set_index('name', inplace=True)  # Set 'name' as index
    merged_df.to_csv(output_file)  # Save as CSV

def main():
    parser = argparse.ArgumentParser(description="Create a relative abundance matrix from Bracken files.")
    parser.add_argument("--input_files", nargs="+", required=True, help="List of Bracken files.")
    parser.add_argument("--output", required=True, help="Output CSV file.")
    args = parser.parse_args()

    create_abundance_matrix(args.input_files, args.output)

if __name__ == "__main__":
    main()
