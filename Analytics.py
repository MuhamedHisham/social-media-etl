import pandas as pd
import os
from datetime import datetime

INPUT_FILE = "unified_posts_transformed.csv"

DAILY_METRICS_FILE = "daily_engagement_metrics.csv"
TOP_POSTS_FILE = "top_5_posts_overall.csv"
TOP_PER_PLATFORM_FILE = "top_3_posts_per_platform.csv"
MOVING_AVG_FILE = "moving_avg_engagement.csv"

def append_or_create(df, filename):
    """Append to existing CSV or create a new one if it doesn't exist."""
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', index=False, header=False)
    else:
        df.to_csv(filename, index=False)

run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

daily_metrics = (
    df.groupby([df["timestamp"].dt.date, "Platform"])
    .agg(
        total_engagement=("Engagement_Score", "sum"),
        avg_engagement=("Engagement_Score", "mean"),
        post_count=("post_id", "count")
    )
    .reset_index()
    .rename(columns={"timestamp": "date"})
)
daily_metrics["generated_at"] = run_time
append_or_create(daily_metrics, DAILY_METRICS_FILE)

top_5_overall = (
    df.sort_values("Engagement_Score", ascending=False)
    .head(5)
)
top_5_overall["generated_at"] = run_time
append_or_create(top_5_overall, TOP_POSTS_FILE)

top_3_per_platform = (
    df.sort_values(["Platform", "Engagement_Score"], ascending=[True, False])
    .groupby("Platform")
    .head(3)
)
top_3_per_platform["generated_at"] = run_time
append_or_create(top_3_per_platform, TOP_PER_PLATFORM_FILE)

df_sorted = df.dropna(subset=["timestamp"]).sort_values("timestamp")

moving_avg_list = []
for platform, g in df_sorted.groupby("Platform"):
    g = g.set_index("timestamp").resample("D")["Engagement_Score"].mean()
    if not g.empty:
        g_ma = g.rolling(window=7, min_periods=1).mean().reset_index()
        g_ma["Platform"] = platform
        g_ma["generated_at"] = run_time
        moving_avg_list.append(g_ma)

if moving_avg_list:
    moving_avg = pd.concat(moving_avg_list, ignore_index=True)
    append_or_create(moving_avg, MOVING_AVG_FILE)

print("Analytics complete. Results appended to CSV files with generation timestamp.")
