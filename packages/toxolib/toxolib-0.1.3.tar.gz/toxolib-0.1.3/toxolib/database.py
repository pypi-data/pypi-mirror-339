"""
Database management functions for toxolib
"""
import os
import logging
import subprocess
import shutil
import tempfile
import requests
from pathlib import Path
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Database URLs
KRAKEN2_DB_URL = "https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz"
CORN_DB_URL = "https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip"

def download_file(url, output_path, desc=None):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f, tqdm(
            desc=desc,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
        for data in response.iter_content(block_size):
            size = f.write(data)
            bar.update(size)
    
    return output_path

def setup_kraken2_db(output_dir, force=False):
    """Download and extract Kraken2 database
    
    Args:
        output_dir (str): Directory to store the database
        force (bool): Force re-download even if the database exists
        
    Returns:
        str: Path to the Kraken2 database directory
    """
    output_dir = os.path.abspath(output_dir)
    db_dir = os.path.join(output_dir, "kraken2-microbial-fatfree")
    
    # Check if database already exists
    if os.path.exists(db_dir) and not force:
        logging.info(f"Kraken2 database already exists at {db_dir}")
        return db_dir
    
    # Create temp directory for download
    temp_dir = tempfile.mkdtemp()
    try:
        # Download database
        db_archive = os.path.join(temp_dir, "k2_standard_20240112.tar.gz")
        logging.info(f"Downloading Kraken2 database to {db_archive}...")
        download_file(KRAKEN2_DB_URL, db_archive, "Downloading Kraken2 DB")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract database
        logging.info(f"Extracting Kraken2 database to {output_dir}...")
        subprocess.run(["tar", "-xzf", db_archive, "-C", output_dir], check=True)
        
        logging.info(f"Kraken2 database setup complete at {db_dir}")
        return db_dir
    
    except Exception as e:
        logging.error(f"Error setting up Kraken2 database: {e}")
        return None
    
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)

def setup_corn_db(output_dir, force=False):
    """Download and extract corn genome database
    
    Args:
        output_dir (str): Directory to store the database
        force (bool): Force re-download even if the database exists
        
    Returns:
        str: Path to the corn database directory
    """
    output_dir = os.path.abspath(output_dir)
    
    # Check if database already exists
    if os.path.exists(output_dir) and os.listdir(output_dir) and not force:
        logging.info(f"Corn genome database already exists at {output_dir}")
        return output_dir
    
    # Create temp directory for download
    temp_dir = tempfile.mkdtemp()
    try:
        # Download database
        db_archive = os.path.join(temp_dir, "corn_db.zip")
        logging.info(f"Downloading corn genome database to {db_archive}...")
        download_file(CORN_DB_URL, db_archive, "Downloading Corn Genome DB")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract database
        logging.info(f"Extracting corn genome database to {output_dir}...")
        subprocess.run(["unzip", "-o", db_archive, "-d", output_dir], check=True)
        
        logging.info(f"Corn genome database setup complete at {output_dir}")
        return output_dir
    
    except Exception as e:
        logging.error(f"Error setting up corn genome database: {e}")
        return None
    
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)

def setup_databases(base_dir, setup_kraken=True, setup_corn=True, force=False):
    """Set up all required databases
    
    Args:
        base_dir (str): Base directory to store databases
        setup_kraken (bool): Whether to set up Kraken2 database
        setup_corn (bool): Whether to set up corn genome database
        force (bool): Force re-download even if databases exist
        
    Returns:
        tuple: (kraken2_db_dir, corn_db_dir)
    """
    kraken2_db_dir = None
    corn_db_dir = None
    
    if setup_kraken:
        kraken2_db_dir = setup_kraken2_db(os.path.join(base_dir, "Kraken2_DB"), force)
        if kraken2_db_dir:
            # Set environment variable for Kraken2
            os.environ["KRAKEN2_DB_DIR"] = os.path.dirname(kraken2_db_dir)
    
    if setup_corn:
        corn_db_dir = setup_corn_db(os.path.join(base_dir, "corn_db"), force)
    
    return kraken2_db_dir, corn_db_dir
