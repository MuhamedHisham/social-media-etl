import requests
import pandas as pd
import os

# ---- CONFIG ----
BEARER_TOKEN = "YOUR_BEARER_TOKEN"
KEYWORDS = ["AI", "technology", "robotics", "gaming"]
MAX_RESULTS = 10
OUTPUT_FILE = "X_API_L.csv"

headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# ---- Load existing CSV ----
if os.path.exists(OUTPUT_FILE):
    existing_df = pd.read_csv(OUTPUT_FILE, dtype=str)
    existing_ids = set(existing_df['Post_ID'])
else:
    existing_df = pd.DataFrame()
    existing_ids = set()

rows = []

# ---- Fetch tweets per keyword ----
for query in KEYWORDS:
    url = f"https://api.x.com/2/tweets/search/recent?query={query}&tweet.fields=public_metrics,created_at&expansions=author_id&max_results={MAX_RESULTS}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Request failed for query '{query}': {response.status_code}")
        continue
    data = response.json()

    for tweet in data.get("data", []):
        tweet_id = tweet["id"]
        if tweet_id in existing_ids:
            continue

        text = tweet["text"]
        author_id = tweet["author_id"]
        created_at = tweet["created_at"]
        likes = tweet["public_metrics"]["like_count"]
        retweets = tweet["public_metrics"]["retweet_count"]
        replies = tweet["public_metrics"]["reply_count"]
        quotes = tweet["public_metrics"]["quote_count"]

        rows.append({
            "Platform": "X",
            "Author_ID": author_id,
            "Post_ID": tweet_id,
            "Content": text,
            "Likes": likes,
            "Comments": replies,
            "Shares/Retweets": retweets,
            "Quotes": quotes,
            "Post_Date": created_at
        })

# ---- Append to existing CSV ----
if rows:
    new_df = pd.DataFrame(rows)
    if not existing_df.empty:
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df
    # Use double quotes for text fields and escape properly
    updated_df.to_csv(OUTPUT_FILE, index=False, quoting=pd.io.common.csv.QUOTE_ALL)
    print(f"✅ Added {len(new_df)} new tweets. Total tweets: {len(updated_df)}")
else:
    print("✅ No new tweets to add. CSV is up-to-date.")
