import subprocess

def main():
    # Step 1: Fetch YouTube data
    print("🔹 Fetching YouTube data...")
    subprocess.run(["python", "YouTube_API_E.py"], check=True)

    # Step 2: Fetch X/Twitter data
    print("🔹 Fetching X/Twitter data...")
    subprocess.run(["python", "X_API_E.py"], check=True)

    # Step 3: Run ETL pipeline
    print("🔹 Running ETL pipeline...")
    subprocess.run(["python", "ETL_Pipeline.py"], check=True)

    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()
    