# run_all.py
import os
import subprocess
import time

from config import (
    RETRY_COUNT,
    RETRY_DELAY,
    WAIT_TIME_BETWEEN_SCRIPTS
)

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    """
    Run a script with retry logic and a delay.
    """
    attempt = 0
    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} completed successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"{script_name} failed after {retries} attempts.")
                raise e

def setup_infrastructure():
    """Create ECS cluster and verify its creation."""
    try:
        # Create ECS cluster
        cluster_name = os.getenv("ECS_CLUSTER", "default")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        print(f"Creating ECS cluster: {cluster_name}")
        subprocess.run([
            "aws", "ecs", "create-cluster",
            "--cluster-name", cluster_name,
            "--region", aws_region
        ], check=True)

        # Verify cluster creation
        print(f"Verifying cluster {cluster_name}...")
        subprocess.run([
            "aws", "ecs", "describe-clusters",
            "--clusters", cluster_name,
            "--region", aws_region
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Infrastructure setup failed: {e}")
        raise

def main():
    try:
        # Step 0: Infrastructure setup
        setup_infrastructure()

        # Step 1: Fetch highlights
        run_script("fetch.py")
        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 2: Process videos
        run_script("process_videos.py")
        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 3: MediaConvert processing
        run_script("mediaconvert_process.py")

        print("All scripts executed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
