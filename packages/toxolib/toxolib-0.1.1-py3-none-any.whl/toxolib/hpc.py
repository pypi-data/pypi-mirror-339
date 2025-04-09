"""
Module for HPC integration with toxolib
"""
import os
import sys
import logging
import subprocess
import paramiko
import getpass
from pathlib import Path
import yaml
import time
from .abundance_matrix import create_abundance_matrix

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class HPCConnection:
    """Class to handle HPC connections and job submission"""
    
    def __init__(self, config_file=None):
        """Initialize HPC connection with configuration"""
        self.config = {}
        self.ssh = None
        self.sftp = None
        
        # If config file is provided, load it
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        else:
            # Default config file in user's home directory
            default_config = os.path.expanduser("~/.toxolib/hpc_config.yaml")
            if os.path.exists(default_config):
                self.load_config(default_config)
    
    def load_config(self, config_file):
        """Load HPC configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            logging.info(f"Loaded HPC configuration from {config_file}")
        except Exception as e:
            logging.error(f"Error loading HPC configuration: {e}")
            self.config = {}
    
    def save_config(self, config_file=None):
        """Save HPC configuration to YAML file"""
        if not config_file:
            # Default config file in user's home directory
            config_dir = os.path.expanduser("~/.toxolib")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "hpc_config.yaml")
        
        try:
            with open(config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            logging.info(f"Saved HPC configuration to {config_file}")
            return True
        except Exception as e:
            logging.error(f"Error saving HPC configuration: {e}")
            return False
    
    def setup_connection(self, hostname=None, username=None, password=None, key_file=None):
        """Set up SSH connection to HPC"""
        # Use provided values or get from config
        hostname = hostname or self.config.get('hostname')
        username = username or self.config.get('username')
        key_file = key_file or self.config.get('key_file')
        
        # If any required values are missing, prompt user
        if not hostname:
            hostname = input("Enter HPC hostname: ")
        if not username:
            username = input(f"Enter username for {hostname}: ")
        
        # Update config
        self.config['hostname'] = hostname
        self.config['username'] = username
        
        if key_file and os.path.exists(os.path.expanduser(key_file)):
            self.config['key_file'] = key_file
        
        # Connect to HPC
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if key_file and os.path.exists(os.path.expanduser(key_file)):
                # Connect with key file
                self.ssh.connect(
                    hostname=hostname,
                    username=username,
                    key_filename=os.path.expanduser(key_file)
                )
                logging.info(f"Connected to {hostname} using key file")
            else:
                # Connect with password
                if not password:
                    password = getpass.getpass(f"Enter password for {username}@{hostname}: ")
                
                self.ssh.connect(
                    hostname=hostname,
                    username=username,
                    password=password
                )
                logging.info(f"Connected to {hostname} using password")
            
            # Create SFTP connection
            self.sftp = self.ssh.open_sftp()
            
            # Test connection
            _, stdout, _ = self.ssh.exec_command("echo 'Connection successful'")
            output = stdout.read().decode().strip()
            
            if output == 'Connection successful':
                logging.info("HPC connection test successful")
                return True
            else:
                logging.error("HPC connection test failed")
                return False
                
        except Exception as e:
            logging.error(f"Error connecting to HPC: {e}")
            return False
    
    def close_connection(self):
        """Close SSH and SFTP connections"""
        if self.sftp:
            self.sftp.close()
            self.sftp = None
        
        if self.ssh:
            self.ssh.close()
            self.ssh = None
        
        logging.info("HPC connection closed")
    
    def upload_file(self, local_path, remote_path):
        """Upload a file to HPC"""
        if not self.sftp:
            logging.error("No SFTP connection. Please set up connection first.")
            return False
        
        try:
            # Create remote directory if it doesn't exist
            remote_dir = os.path.dirname(remote_path)
            self.ssh.exec_command(f"mkdir -p {remote_dir}")
            
            # Upload file
            self.sftp.put(local_path, remote_path)
            logging.info(f"Uploaded {local_path} to {remote_path}")
            return True
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            return False
    
    def download_file(self, remote_path, local_path):
        """Download a file from HPC"""
        if not self.sftp:
            logging.error("No SFTP connection. Please set up connection first.")
            return False
        
        try:
            # Create local directory if it doesn't exist
            local_dir = os.path.dirname(local_path)
            os.makedirs(local_dir, exist_ok=True)
            
            # Download file
            self.sftp.get(remote_path, local_path)
            logging.info(f"Downloaded {remote_path} to {local_path}")
            return True
        except Exception as e:
            logging.error(f"Error downloading file: {e}")
            return False
    
    def execute_command(self, command):
        """Execute a command on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Execute command
            _, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                logging.warning(f"Command execution warning: {error}")
            
            return output
        except Exception as e:
            logging.error(f"Error executing command: {e}")
            return None
    
    def check_file_exists(self, remote_path):
        """Check if a file exists on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return False
        
        try:
            # Check if file exists
            _, stdout, _ = self.ssh.exec_command(f"test -f {remote_path} && echo 'exists'")
            output = stdout.read().decode().strip()
            
            return output == 'exists'
        except Exception as e:
            logging.error(f"Error checking file existence: {e}")
            return False
    
    def submit_job(self, job_script_path, job_name=None):
        """Submit a job to HPC using sbatch"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Submit job
            job_name_arg = f"-J {job_name}" if job_name else ""
            _, stdout, stderr = self.ssh.exec_command(f"sbatch {job_name_arg} {job_script_path}")
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                logging.error(f"Job submission error: {error}")
                return None
            
            # Extract job ID from output (e.g., "Submitted batch job 123456")
            if "Submitted batch job" in output:
                job_id = output.split()[-1]
                logging.info(f"Job submitted with ID: {job_id}")
                return job_id
            else:
                logging.error(f"Unexpected job submission output: {output}")
                return None
        except Exception as e:
            logging.error(f"Error submitting job: {e}")
            return None
    
    def check_job_status(self, job_id):
        """Check the status of a job on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Check job status
            _, stdout, _ = self.ssh.exec_command(f"sacct -j {job_id} --format=State --noheader | head -1")
            status = stdout.read().decode().strip()
            
            if status:
                logging.info(f"Job {job_id} status: {status}")
                return status
            else:
                logging.warning(f"No status found for job {job_id}")
                return None
        except Exception as e:
            logging.error(f"Error checking job status: {e}")
            return None
    
    def wait_for_job_completion(self, job_id, check_interval=60, timeout=None):
        """Wait for a job to complete on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return False
        
        start_time = time.time()
        logging.info(f"Waiting for job {job_id} to complete...")
        
        while True:
            # Check if timeout has been reached
            if timeout and (time.time() - start_time) > timeout:
                logging.error(f"Timeout waiting for job {job_id} to complete")
                return False
            
            # Check job status
            status = self.check_job_status(job_id)
            
            if status in ['COMPLETED']:
                logging.info(f"Job {job_id} completed successfully")
                return True
            elif status in ['FAILED', 'CANCELLED', 'TIMEOUT', 'NODE_FAIL']:
                logging.error(f"Job {job_id} failed with status: {status}")
                return False
            elif status in ['RUNNING', 'PENDING', 'CONFIGURING']:
                # Job still running, wait and check again
                logging.info(f"Job {job_id} is {status}. Checking again in {check_interval} seconds...")
                time.sleep(check_interval)
            else:
                logging.warning(f"Unknown job status: {status}. Checking again in {check_interval} seconds...")
                time.sleep(check_interval)

def generate_job_script(snakemake_file, output_dir, job_name="toxolib_job", partition="normal", threads=32, memory=200, time="144:00:00"):
    """Generate a SLURM job script for running Snakemake on HPC
    
    Args:
        snakemake_file (str): Path to the Snakemake file on HPC
        output_dir (str): Output directory on HPC
        job_name (str): Name of the job
        partition (str): SLURM partition to use
        threads (int): Number of CPU threads to request
        memory (int): Memory in GB to request
        time (str): Time limit for the job in format HH:MM:SS
    """
    script = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={output_dir}/logs/{job_name}_%j.out
#SBATCH --error={output_dir}/logs/{job_name}_%j.err
#SBATCH --time={time}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={threads}
#SBATCH --mem={memory}G
#SBATCH --partition={partition}

# Create output directories
mkdir -p {output_dir}/logs

# Load Anaconda module (customize for your HPC)
module load anaconda3

# Create conda environment if it doesn't exist
CONDA_ENV_DIR="{output_dir}/conda_env"
if [ ! -d "$CONDA_ENV_DIR" ]; then
    echo "Creating conda environment..."
    conda env create -f {output_dir}/environment.yml -p $CONDA_ENV_DIR
    if [ $? -ne 0 ]; then
        echo "Failed to create conda environment"
        exit 1
    fi
    echo "Conda environment created successfully"
fi

# Activate conda environment
echo "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $CONDA_ENV_DIR

# Check if environment was activated successfully
if [ $? -ne 0 ]; then
    echo "Failed to activate conda environment"
    exit 1
fi

echo "Using Python: $(which python)"
echo "Python version: $(python --version)"
echo "Using Snakemake: $(which snakemake)"
echo "Snakemake version: $(snakemake --version)"

# Run Snakemake
cd $(dirname {snakemake_file})
snakemake -s {os.path.basename(snakemake_file)} --cores $SLURM_CPUS_PER_TASK

# Check if job completed successfully
if [ $? -eq 0 ]; then
    echo "Job completed successfully"
    exit 0
else
    echo "Job failed"
    exit 1
fi
"""
    return script

def update_snakemake_paths(snakemake_file, raw_data_files, output_dir, kraken_db_dir, corn_db_dir):
    """Update paths in Snakemake file for HPC execution"""
    with open(snakemake_file, 'r') as f:
        content = f.read()
    
    # Update directories
    content = content.replace("RAW_DATA_DIR = \"/home/dac6360/Toxonomy/Raw_Data\"", f"RAW_DATA_DIR = \"{output_dir}/Raw_Data\"")
    content = content.replace("PREPROCESSED_DATA_DIR = \"/home/dac6360/Toxonomy/Preprocessed_Data\"", f"PREPROCESSED_DATA_DIR = \"{output_dir}/Preprocessed_Data\"")
    content = content.replace("KRAKEN2_DB_DIR = \"/home/dac6360/Toxonomy/Kraken2_DB\"", f"KRAKEN2_DB_DIR = \"{kraken_db_dir}\"")
    
    # Update other directories
    for dir_name in ["KRAKEN2_DNA_DIR", "BRACKEN_DNA_DIR", "PYTHON_BRACKEN_TO_KRONA_DIR", 
                    "PYTHON_ALPHA_BETA_DIVERSITY_DIR", "PYTHON_RELATIVE_ABUNDANCE_MATRIX_DIR",
                    "FASTP_LOGS_DIR", "BOWTIE2_HOST_LOGS_DIR", "KRAKEN2_DB_LOGS_DIR",
                    "KRAKEN2_DNA_LOGS_DIR", "BRACKEN_DNA_LOGS_DIR", "PYTHON_BRACKEN_TO_KRONA_LOGS_DIR",
                    "PYTHON_ALPHA_BETA_DIVERSITY_LOGS_DIR", "PYTHON_RELATIVE_ABUNDANCE_MATRIX_LOGS_DIR"]:
        content = content.replace(f"{dir_name} = \"/home/dac6360/Toxonomy/", f"{dir_name} = \"{output_dir}/")
    
    # Update corn_db path
    content = content.replace("params.index_prefix = \"/home/dac6360/Toxonomy/corn_db/corn_db\"", f"params.index_prefix = \"{corn_db_dir}/corn_db\"")
    
    # Update sample list based on input files
    sample_names = []
    for raw_file in raw_data_files:
        # Extract sample name from filename (assuming format like sample_R1.fastq.gz)
        base_name = os.path.basename(raw_file)
        sample_name = base_name.split('_')[0]
        if sample_name not in sample_names:
            sample_names.append(sample_name)
    
    # Replace SAMPLES list
    samples_str = ", ".join([f'"{s}"' for s in sample_names])
    content = content.replace("SAMPLES = [\"S1\", \"S2\", \"S3\", \"S4\", \"S5\", \"S6\", \"S7\", \"S8\", \"S9\", \"S10\", \n           \"S11\", \"S12\", \"S13\", \"S14\", \"S15\", \"S16\", \"S17\", \"S18\", \"S19\", \"S20\", \n           \"S21\", \"S22\", \"S23\", \"S24\", \"S25\", \"S26\"]", f"SAMPLES = [{samples_str}]")
    
    # Write updated content back to file
    with open(snakemake_file, 'w') as f:
        f.write(content)
    
    return True

def run_on_hpc(raw_files, output_dir, kraken_db_dir=None, corn_db_dir=None, config_file=None, partition="normal", threads=32, memory=200, time="144:00:00"):
    """Run the toxolib workflow on HPC"""
    # Initialize HPC connection
    hpc = HPCConnection(config_file)
    
    # If not connected, set up connection
    if not hpc.ssh:
        if not hpc.setup_connection():
            logging.error("Failed to connect to HPC")
            return False
    
    try:
        # Create remote directories
        remote_output_dir = output_dir
        remote_raw_data_dir = f"{remote_output_dir}/Raw_Data"
        remote_scripts_dir = f"{remote_output_dir}/scripts"
        
        hpc.execute_command(f"mkdir -p {remote_raw_data_dir} {remote_scripts_dir}")
        
        # Upload raw data files
        logging.info("Uploading raw data files to HPC...")
        for raw_file in raw_files:
            remote_file = f"{remote_raw_data_dir}/{os.path.basename(raw_file)}"
            hpc.upload_file(raw_file, remote_file)
        
        # Upload Snakemake file
        local_snakemake = os.path.join(os.path.dirname(__file__), "data", "Snakefile")
        remote_snakemake = f"{remote_output_dir}/Snakefile"
        hpc.upload_file(local_snakemake, remote_snakemake)
        
        # Upload create_abundance_matrix.py script
        local_script = os.path.join(os.path.dirname(__file__), "data", "create_abundance_matrix.py")
        remote_script = f"{remote_scripts_dir}/create_abundance_matrix.py"
        hpc.upload_file(local_script, remote_script)
        
        # Upload environment.yml file for conda environment creation
        local_env_file = os.path.join(os.path.dirname(__file__), "data", "environment.yml")
        remote_env_file = f"{remote_output_dir}/environment.yml"
        hpc.upload_file(local_env_file, remote_env_file)
        logging.info("Uploaded environment.yml for conda environment creation")
        
        # Update paths in Snakemake file
        logging.info("Updating paths in Snakemake file...")
        # First download the file
        temp_snakemake = "/tmp/Snakefile.tmp"
        hpc.download_file(remote_snakemake, temp_snakemake)
        
        # Update paths
        update_snakemake_paths(
            temp_snakemake, 
            raw_files, 
            remote_output_dir, 
            kraken_db_dir or f"{remote_output_dir}/Kraken2_DB", 
            corn_db_dir or f"{remote_output_dir}/corn_db"
        )
        
        # Upload updated file
        hpc.upload_file(temp_snakemake, remote_snakemake)
        os.remove(temp_snakemake)
        
        # Generate and upload job script
        logging.info("Generating job script...")
        job_script = generate_job_script(
            remote_snakemake, 
            remote_output_dir,
            partition=partition,
            threads=threads,
            memory=memory,
            time=time
        )
        job_script_path = f"{remote_output_dir}/run_toxolib.sh"
        
        with open("/tmp/run_toxolib.sh", "w") as f:
            f.write(job_script)
        
        hpc.upload_file("/tmp/run_toxolib.sh", job_script_path)
        os.remove("/tmp/run_toxolib.sh")
        
        # Make job script executable
        hpc.execute_command(f"chmod +x {job_script_path}")
        
        # Submit job
        logging.info("Submitting job to HPC...")
        job_id = hpc.submit_job(job_script_path)
        
        if not job_id:
            logging.error("Failed to submit job")
            return False
        
        # Wait for job completion
        logging.info(f"Job submitted with ID: {job_id}")
        logging.info("You can check job status using: toxolib hpc-status --job-id JOB_ID")
        logging.info("Or download results using: toxolib hpc-download --job-id JOB_ID --output-dir LOCAL_DIR")
        
        return job_id
        
    except Exception as e:
        logging.error(f"Error running on HPC: {e}")
        return False
    finally:
        # Close connection
        hpc.close_connection()

def download_results(job_id, local_dir, config_file=None):
    """Download results from HPC after job completion"""
    # Initialize HPC connection
    hpc = HPCConnection(config_file)
    
    # If not connected, set up connection
    if not hpc.ssh:
        if not hpc.setup_connection():
            logging.error("Failed to connect to HPC")
            return False
    
    try:
        # Check job status
        status = hpc.check_job_status(job_id)
        
        if status != 'COMPLETED':
            logging.error(f"Job {job_id} has not completed successfully. Status: {status}")
            return False
        
        # Get job details to find output directory
        _, stdout, _ = hpc.ssh.exec_command(f"sacct -j {job_id} --format=WorkDir --noheader | head -1")
        work_dir = stdout.read().decode().strip()
        
        if not work_dir:
            logging.error(f"Could not determine working directory for job {job_id}")
            return False
        
        # Determine output directory based on working directory
        output_dir = os.path.dirname(work_dir)
        abundance_matrix = f"{output_dir}/Results/Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/relative_abundance_matrix_species.csv"
        
        # Check if abundance matrix exists
        if not hpc.check_file_exists(abundance_matrix):
            logging.error(f"Abundance matrix not found at {abundance_matrix}")
            return False
        
        # Create local directory
        os.makedirs(local_dir, exist_ok=True)
        
        # Download abundance matrix
        local_matrix = os.path.join(local_dir, "abundance_matrix.csv")
        if not hpc.download_file(abundance_matrix, local_matrix):
            logging.error("Failed to download abundance matrix")
            return False
        
        logging.info(f"Downloaded abundance matrix to {local_matrix}")
        return local_matrix
        
    except Exception as e:
        logging.error(f"Error downloading results: {e}")
        return False
    finally:
        # Close connection
        hpc.close_connection()
