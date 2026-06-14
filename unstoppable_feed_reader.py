import requests
import xml.etree.ElementTree as ET
import json
import os

OUTPUT_DIR = "data_storage/downloaded_datasets/pro_scrapes/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# বাংলাদেশি সাইটগুলোর আরএসএস ফিড লিংক
FEEDS = [
    {"name": "factwatch_bd", "url": "https://factwatch.bd/feed/"},
    {"name": "boom_bd", "url": "https://boombangladesh.com/feed/"}
]

def get_feed_data():
    for feed in FEEDS:
        print(f"📡 Fetching Feed: {feed['name']}...")
        try:
            response = requests.get(feed['url'], timeout=15)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = []
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    items.append({"claim_text": title, "verdict": "UNVERIFIED", "repo_source": feed['name']})
                
                with open(f"{OUTPUT_DIR}/{feed['name']}_feed.jsonl", 'w', encoding='utf-8') as f:
                    for entry in items:
                        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                print(f"✅ Success: Fetched {len(items)} items from {feed['name']}")
            else:
                print(f"❌ Failed to reach feed: {feed['name']}")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    get_feed_data()
