import subprocess
import sys
import os
import time

def run_step(command, step_name):
    print(f"\n{'='*50}")
    print(f"Running Step: {step_name}")
    print(f"Command: {command}")
    print(f"{'='*50}\n")
    
    try:
        # Use shell=True for Windows compatibility with some commands, 
        # but list format is generally safer. Splitting string for simplicity here.
        result = subprocess.run(command, shell=True, check=True, text=True)
        print(f"\n[SUCCESS] {step_name} completed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {step_name} failed with exit code {e.returncode}.")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Ingestion (Python)
    ingestion_script = os.path.join(base_dir, "ingestion", "DataIngestionService.py")
    if not run_step(f"python \"{ingestion_script}\"", "1. Data Ingestion"):
        sys.exit(1)

    # 2. Filtering (TypeScript)
    # Assumes ts-node is available globally or via npx
    filtering_script = os.path.join(base_dir, "filtering", "SemanticFilter.ts")
    # Using npx ts-node to avoid global dependency issues if possible, or just ts-node
    if not run_step(f"npx ts-node \"{filtering_script}\"", "2. Semantic Filtering"):
        sys.exit(1)

    # 3. Digest Generation (Go)
    digest_script = os.path.join(base_dir, "digest", "DigestArchitect.go")
    if not run_step(f"go run \"{digest_script}\"", "3. Digest Generation"):
        sys.exit(1)

    print("\n" + "="*50)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*50)
    
    # Optional: Open the result
    result_file = os.path.join(base_dir, "index.html")
    if os.path.exists(result_file):
        print(f"Opening {result_file}...")
        if sys.platform == "win32":
            os.startfile(result_file)
        elif sys.platform == "darwin":
            subprocess.run(["open", result_file])
        else:
            subprocess.run(["xdg-open", result_file])

if __name__ == "__main__":
    main()
