import subprocess
import os
from datetime import datetime

def run_script(script):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{script}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_file, "w") as f:
        subprocess.run(["python", script], check=True, stdout=f, stderr=f)

def main():
    print("🔹 Fetching YouTube data...")
    run_script("YouTube_API_E.py")

    print("🔹 Fetching X/Twitter data...")
    run_script("X_API_E.py")

    print("🔹 Running ETL pipeline...")
    run_script("ETL_Pipeline.py")

    print("🔹 Running Analytics...")
    run_script("Analytics.py")

    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()
