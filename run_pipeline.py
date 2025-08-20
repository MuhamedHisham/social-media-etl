import subprocess

def main():
    print("🔹 Fetching YouTube data...")
    subprocess.run(["python", "YouTube_API_E.py"], check=True)

    print("🔹 Fetching X/Twitter data...")
    subprocess.run(["python", "X_API_E.py"], check=True)

    print("🔹 Running ETL pipeline...")
    subprocess.run(["python", "ETL_Pipeline.py"], check=True)

    print("🔹 Running Analytics...")
    subprocess.run(["python", "Analytics.py"], check=True)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
    