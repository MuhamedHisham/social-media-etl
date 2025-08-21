📊 Data Engineering Pipeline

This project implements a data engineering pipeline that collects, transforms, and analyzes social media engagement data. The pipeline is built in Python using pandas and outputs structured CSV files for further analysis and reporting.

🚀 Features
✅ Automated data ingestion from multiple CSV sources
✅ Data cleaning & transformation (sorting, deduplication, formatting)
✅ Analytics generation (engagement metrics, moving averages, trends)
✅ Unified outputs saved to CSV for downstream use

📂 Project Structure
Data-Engineering-Project/
│── Extracted_files/              # Raw extracted data
│── Transformed_files/            # Cleaned & transformed CSVs
│── unified_posts_transformed.csv # Final merged dataset
│── Extracted_files.py            # Extract script
│── Transformed_files.py          # Transform script
│── Analytics.py                  # Analytics & reporting script
│── requirements.txt              # Python dependencies
│── README.md                     # Project documentation

⚙️ Installation
Clone this repository:
git clone https://github.com/your-username/data-engineering-pipeline.git
cd data-engineering-pipeline

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt

▶️ Usage
Run the pipeline step by step or all at once:

1. Extract
python Extracted_files.py

2. Transform
python Transformed_files.py

3. Analytics
python Analytics.py

📊 Example Output

The pipeline generates cleaned CSVs with columns such as:

title → Post title

views → Number of views

likes → Number of likes

comments → Comment count

engagement → Computed engagement metric

date → Date of posting

platform → Source platform

Example row:

title	views	likes	comments	engagement	date	platform	channel_id	video_id
Ditching Microsoft for Startup	243	12	0	255.0	2025-05-09 09:00:32	YouTube	UC8butISFwT-Wl7EV0hUK0BQ	FHLmuNj20
📌 Notes

The CSV files in the same must be provided before running the pipeline.

All outputs will be generated in the same directory.

Final dataset is saved as unified_posts_transformed.csv.

👨‍💻 Author

Muhamed Hisham

💼 www.linkedin.com/in/muhamed-hisham-a49961101
📧 muhamed.hisham.ahmed@gmail.com

