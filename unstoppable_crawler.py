import feedparser
import json
import os
import time

# ডাটা স্টোরেজ পাথ
OUTPUT_DIR = "data_storage/downloaded_datasets/recent_scrapes/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# বাংলাদেশের প্রধান ফ্যাক্ট-চেক ও নিউজ সাইটের RSS ফিড
SOURCES = {
    "factwatch_bd": "https://factwatch.bd/feed/", 
    "bdnews24": "https://bdnews24.com/feed",
    "prothomalo": "https://www.prothomalo.com/feed/"
}

def fetch_rss_data(source_name, rss_url):
    print(f"🚀 Scraping started for: {source_name}")
    try:
        feed = feedparser.parse(rss_url)
        file_path = os.path.join(OUTPUT_DIR, f"{source_name}_data.jsonl")
        
        count = 0
        with open(file_path, 'a', encoding='utf-8') as f:
            for entry in feed.entries:
                data = {
                    "claim_text": entry.title,
                    "verdict": "UNVERIFIED",
                    "evidence_text": entry.summary,
                    "repo_source": source_name,
                    "url": entry.link
                }
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
                count += 1
        print(f"✅ Successfully saved {count} records from {source_name}")
        
    except Exception as e:
        print(f"❌ Failed to scrape {source_name}: {e}")

if __name__ == "__main__":
    for name, url in SOURCES.items():
        fetch_rss_data(name, url)
        time.sleep(3)
