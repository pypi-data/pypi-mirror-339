"""
Command-line interface for toxolib
"""
import argparse
import sys
import os
import logging
from pathlib import Path
from .abundance_matrix import process_raw_data, create_abundance_matrix, check_dependencies
from .hpc import HPCConnection, run_on_hpc, download_results
from .database import setup_databases, setup_kraken2_db, setup_corn_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def print_banner():
    """Print the toxolib banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ████████╗ ██████╗ ██╗  ██╗ ██████╗ ██╗     ██╗██████╗   ║
    ║   ╚══██╔══╝██╔═══██╗╚██╗██╔╝██╔═══██╗██║     ██║██╔══██╗  ║
    ║      ██║   ██║   ██║ ╚███╔╝ ██║   ██║██║     ██║██████╔╝  ║
    ║      ██║   ██║   ██║ ██╔██╗ ██║   ██║██║     ██║██╔══██╗  ║
    ║      ██║   ╚██████╔╝██╔╝ ██╗╚██████╔╝███████╗██║██████╔╝  ║
    ║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═════╝   ║
    ║                                                            ║
    ║   Metagenomic Taxonomic Profiling & Abundance Matrix Tool  ║
    ║                         v0.1.4                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point for the toxolib CLI"""
    # Only print banner for actual commands, not for help
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        print_banner()
    
    parser = argparse.ArgumentParser(
        description="toxolib - A tool for metagenomic taxonomic profiling and abundance matrix generation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Abundance matrix from raw data command
    abundance_parser = subparsers.add_parser(
        "abundance", help="Generate abundance matrix from raw data"
    )
    abundance_parser.add_argument(
        "-r", "--raw-files", nargs="+", required=True,
        help="Raw fastq files (can be gzipped)"
    )
    abundance_parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Output directory"
    )
    abundance_parser.add_argument(
        "-t", "--threads", type=int, default=8,
        help="Number of threads to use (default: 8)"
    )
    
    # Direct abundance matrix creation from Bracken files
    matrix_parser = subparsers.add_parser(
        "matrix", help="Create abundance matrix from existing Bracken files"
    )
    matrix_parser.add_argument(
        "-i", "--input-files", nargs="+", required=True,
        help="List of Bracken files"
    )
    matrix_parser.add_argument(
        "-o", "--output", required=True,
        help="Output CSV file"
    )
    
    # Add version command
    version_parser = subparsers.add_parser(
        "version", help="Show version information"
    )
    
    # HPC commands
    hpc_parser = subparsers.add_parser(
        "hpc", help="Run on HPC cluster"
    )
    hpc_parser.add_argument(
        "-r", "--raw-files", nargs="+", required=True,
        help="Raw fastq files (can be gzipped)"
    )
    hpc_parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Output directory on HPC"
    )
    hpc_parser.add_argument(
        "--kraken-db", 
        help="Path to Kraken2 database on HPC"
    )
    hpc_parser.add_argument(
        "--corn-db", 
        help="Path to corn database on HPC"
    )
    hpc_parser.add_argument(
        "--setup-kraken-db", action="store_true",
        help="Download and setup Kraken2 database on HPC"
    )
    hpc_parser.add_argument(
        "--setup-corn-db", action="store_true",
        help="Download and setup corn genome database on HPC"
    )
    hpc_parser.add_argument(
        "--config", 
        help="Path to HPC configuration file"
    )
    
    # HPC job configuration
    hpc_parser.add_argument(
        "--partition",
        default="normal",
        help="SLURM partition to use (default: normal)"
    )
    hpc_parser.add_argument(
        "--threads",
        type=int,
        default=32,
        help="Number of CPU threads to request (default: 32)"
    )
    hpc_parser.add_argument(
        "--memory",
        type=int,
        default=200,
        help="Memory in GB to request (default: 200)"
    )
    hpc_parser.add_argument(
        "--time",
        default="144:00:00",
        help="Time limit for the job in format HH:MM:SS (default: 144:00:00)")
    
    # HPC setup command
    hpc_setup_parser = subparsers.add_parser(
        "hpc-setup", help="Set up HPC connection"
    )
    hpc_setup_parser.add_argument(
        "--hostname", required=True,
        help="HPC hostname"
    )
    hpc_setup_parser.add_argument(
        "--username", required=True,
        help="HPC username"
    )
    hpc_setup_parser.add_argument(
        "--key-file",
        help="Path to SSH key file"
    )
    
    # HPC status command
    hpc_status_parser = subparsers.add_parser(
        "hpc-status", help="Check HPC job status"
    )
    hpc_status_parser.add_argument(
        "--job-id", required=True,
        help="HPC job ID"
    )
    hpc_status_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    
    # HPC download command
    hpc_download_parser = subparsers.add_parser(
        "hpc-download", help="Download results from HPC"
    )
    hpc_download_parser.add_argument(
        "--job-id", required=True,
        help="HPC job ID"
    )
    hpc_download_parser.add_argument(
        "--output-dir", required=True,
        help="Local output directory"
    )
    hpc_download_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    
    # Add database setup command
    db_setup_parser = subparsers.add_parser(
        "db-setup", help="Download and setup databases"
    )
    db_setup_parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Directory to store databases"
    )
    db_setup_parser.add_argument(
        "--kraken", action="store_true",
        help="Download and setup Kraken2 database"
    )
    db_setup_parser.add_argument(
        "--corn", action="store_true",
        help="Download and setup corn genome database"
    )
    db_setup_parser.add_argument(
        "--force", action="store_true",
        help="Force re-download of databases even if they exist"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Handle version command first
    if args.command == "version":
        from . import __version__
        print(f"toxolib version {__version__}")
        sys.exit(0)
    
    # Handle HPC commands
    if args.command == "hpc-setup":
        hpc = HPCConnection()
        if hpc.setup_connection(args.hostname, args.username, key_file=args.key_file):
            hpc.save_config()
            print(f"\n✅ HPC connection set up successfully for {args.username}@{args.hostname}")
            print("Configuration saved to ~/.toxolib/hpc_config.yaml")
        else:
            print("\n❌ Failed to set up HPC connection")
        sys.exit(0)
    
    elif args.command == "hpc-status":
        hpc = HPCConnection(args.config)
        if not hpc.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        status = hpc.check_job_status(args.job_id)
        if status:
            print(f"\nJob {args.job_id} status: {status}")
            if status == "COMPLETED":
                print("\n✅ Job completed successfully")
                print("You can download results using:")
                print(f"  toxolib hpc-download --job-id {args.job_id} --output-dir /path/to/local/dir")
            elif status in ["FAILED", "CANCELLED", "TIMEOUT", "NODE_FAIL"]:
                print("\n❌ Job failed")
            elif status in ["RUNNING", "PENDING", "CONFIGURING"]:
                print("\n⏳ Job is still running")
        else:
            print(f"\n❌ Could not get status for job {args.job_id}")
        sys.exit(0)
        
    elif args.command == "hpc-download":
        result = download_results(args.job_id, args.output_dir, args.config)
        if result:
            print(f"\n✅ Results downloaded successfully to {result}")
        else:
            print("\n❌ Failed to download results")
        sys.exit(0)
        
    elif args.command == "db-setup":
        # Check if at least one database is selected
        if not args.kraken and not args.corn:
            print("\n❌ Please specify at least one database to set up (--kraken or --corn)")
            sys.exit(1)
            
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Setup databases
        kraken_db_dir, corn_db_dir = setup_databases(
            args.output_dir,
            setup_kraken=args.kraken,
            setup_corn=args.corn,
            force=args.force
        )
        
        # Print summary
        print("\n✅ Database setup complete")
        if args.kraken and kraken_db_dir:
            print(f"Kraken2 database: {kraken_db_dir}")
            print(f"Set KRAKEN2_DB_DIR environment variable to: {os.path.dirname(kraken_db_dir)}")
        if args.corn and corn_db_dir:
            print(f"Corn genome database: {corn_db_dir}")
    
    elif args.command == "hpc":
        # Check if raw files exist
        for raw_file in args.raw_files:
            if not os.path.exists(raw_file):
                logging.error(f"Raw file {raw_file} does not exist")
                sys.exit(1)
                
        # Run on HPC
        job_id = run_on_hpc(
            args.raw_files,
            args.output_dir,
            kraken_db_dir=args.kraken_db,
            corn_db_dir=args.corn_db,
            config_file=args.config,
            partition=args.partition,
            threads=args.threads,
            memory=args.memory,
            time=args.time,
            setup_kraken_db=args.setup_kraken_db,
            setup_corn_db=args.setup_corn_db
        )
        
        if job_id:
            print(f"\n✅ Job submitted successfully with ID: {job_id}")
            print("\nYou can check job status using:")
            print(f"  toxolib hpc-status --job-id {job_id}")
            print("\nAnd download results when complete using:")
            print(f"  toxolib hpc-download --job-id {job_id} --output-dir /path/to/local/dir")
        else:
            print("\n❌ Failed to submit job to HPC")
        sys.exit(0)
    
    # Check dependencies for local commands
    if args.command in ["abundance", "matrix"] and not check_dependencies():
        logging.error("Missing required dependencies. Please install them before proceeding.")
        print("\nTip: You can install all dependencies using the provided conda environment:")
        print("  conda env create -f environment.yml")
        print("  conda activate taxonomy_env")
        sys.exit(1)
    
    # Handle commands
    if args.command == "abundance":
        # Check if raw files exist
        for raw_file in args.raw_files:
            if not os.path.exists(raw_file):
                logging.error(f"Raw file {raw_file} does not exist")
                sys.exit(1)
        
        # Process raw data
        try:
            logging.info(f"Starting taxonomic profiling for {len(args.raw_files)} input files...")
            logging.info(f"Output will be saved to: {args.output_dir}")
            
            abundance_file = process_raw_data(
                args.raw_files, args.output_dir, args.threads
            )
            
            logging.info(f"Abundance matrix generated: {abundance_file}")
            print(f"\n✅ Process completed successfully!")
            print(f"Abundance matrix saved to: {abundance_file}")
            print(f"Check the logs directory for detailed information.")
            
        except Exception as e:
            logging.error(f"Error generating abundance matrix: {e}")
            sys.exit(1)
    
    elif args.command == "matrix":
        # Check if input files exist
        for input_file in args.input_files:
            if not os.path.exists(input_file):
                logging.error(f"Input file {input_file} does not exist")
                sys.exit(1)
        
        # Create abundance matrix
        try:
            logging.info(f"Creating abundance matrix from {len(args.input_files)} Bracken files...")
            create_abundance_matrix(args.input_files, args.output)
            
            logging.info(f"Abundance matrix created: {args.output}")
            print(f"\n✅ Abundance matrix created successfully: {args.output}")
            
        except Exception as e:
            logging.error(f"Error creating abundance matrix: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
