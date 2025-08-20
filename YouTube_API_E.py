import requests
import pandas as pd
import os

# ---- CONFIG ----
API_KEY = "AIzaSyCiMQzOEiVUsU8T0kcrY5NtHo6M-KQjZ6o"  # Replace with your key
KEYWORDS = ["Quantum Computing", "AI", "Evolution Theory"]  # Random search queries
MAX_RESULTS = 15  # Max per keyword
OUTPUT_FILE = "YouTube_API_L.csv"

# ---- STEP 0: Load existing CSV if exists ----
if os.path.exists(OUTPUT_FILE):
    existing_df = pd.read_csv(OUTPUT_FILE)
    existing_video_ids = set(existing_df['Video_ID'].astype(str))
else:
    existing_df = pd.DataFrame()
    existing_video_ids = set()

rows = []

# ---- STEP 1: Fetch videos per keyword ----
for query in KEYWORDS:
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&order=date&maxResults={MAX_RESULTS}"
        f"&q={query}&key={API_KEY}"
    )
    response = requests.get(search_url).json()
    videos = response.get("items", [])

    for item in videos:
        video_id = item["id"]["videoId"]
        if video_id in existing_video_ids:
            continue  # skip duplicates

        snippet = item["snippet"]
        title = snippet["title"]
        published_at = snippet["publishedAt"]

        # Fetch video statistics
        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
        stats_response = requests.get(stats_url).json()
        stats = stats_response["items"][0]["statistics"]

        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        shares = 0  # YouTube API does not provide shares
        engagement = likes + comments + shares

        rows.append({
            "Video_ID": video_id,
            "Content": title,
            "Post_DateTime": published_at.replace("T", " ").replace("Z", ""),
            "Likes": likes,
            "Comments": comments,
            "Shares": shares,
            "Engagement_Score": engagement,
            "Platform": "YouTube"
        })

# ---- STEP 2: Append new rows to existing CSV ----
if rows:
    new_df = pd.DataFrame(rows)
    if not existing_df.empty:
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df
    updated_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Added {len(new_df)} new videos. Total videos: {len(updated_df)}")
else:
    print("✅ No new videos to add. CSV is up-to-date.")
