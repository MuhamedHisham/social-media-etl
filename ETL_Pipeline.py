import pandas as pd
import re
import os

# Files
youtube_file = "YouTube_API_L.csv"
x_file = "X_API_L.csv"
unified_file = "unified_posts_transformed.csv"
line_tracker_file = "last_lines.csv"

# Load last processed lines
if os.path.exists(line_tracker_file):
    tracker = pd.read_csv(line_tracker_file, index_col=0).to_dict()["last_line"]
else:
    tracker = {"youtube": 0, "x": 0}

# ---- Load only new lines ----
youtube = pd.read_csv(youtube_file, skiprows=range(1, tracker.get("youtube", 0)+1))
x_data = pd.read_csv(x_file, skiprows=range(1, tracker.get("x", 0)+1))

if youtube.empty and x_data.empty:
    print("✅ No new data to process.")
    exit()

# ---- Transform (same as before) ----
# Normalize columns
youtube = youtube.rename(columns={
    "Video_ID": "post_id",
    "Author/User ID": "author",
    "Post_DateTime": "timestamp",
    "Content": "content",
    "Likes": "likes",
    "Comments": "comments",
    "Shares": "shares"
})
youtube["platform"] = "YouTube"

x_data = x_data.rename(columns={
    "Post_ID": "post_id",
    "Author_ID": "author",
    "Post_Date": "timestamp",
    "Content": "content",
    "Likes": "likes",
    "Comments": "comments",
    "Shares/Retweets": "shares"
})
x_data["platform"] = "X"

# Clean content
def clean_text(text):
    if pd.isna(text):
        return ""
    return re.sub(r'[^\x00-\x7F]+', '', str(text)).strip()

youtube['content'] = youtube['content'].apply(clean_text)
x_data['content'] = x_data['content'].apply(clean_text)

# Combine
unified_new = pd.concat([youtube, x_data], ignore_index=True)

# Timestamps
unified_new['timestamp'] = pd.to_datetime(unified_new['timestamp'], errors='coerce', utc=True)
unified_new['timestamp'] = unified_new['timestamp'].dt.tz_convert(None)
unified_new['timestamp'] = unified_new['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Engagement
unified_new[['likes', 'comments', 'shares']] = unified_new[['likes', 'comments', 'shares']].fillna(0)
unified_new['engagement_score'] = unified_new['likes'] + unified_new['comments'] + unified_new['shares']

# Append to unified CSV
unified_new.to_csv(unified_file, mode='a', index=False, header=not os.path.exists(unified_file))
print(f"✅ Added {len(unified_new)} new rows to {unified_file}")

# Update last processed lines
tracker["youtube"] = sum(1 for _ in open(youtube_file, encoding="utf-8")) - 1
tracker["x"] = sum(1 for _ in open(x_file, encoding="utf-8")) - 1
pd.DataFrame.from_dict(tracker, orient="index", columns=["last_line"]).to_csv(line_tracker_file)
