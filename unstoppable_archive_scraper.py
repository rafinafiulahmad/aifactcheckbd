import requests
import json
import os

OUTPUT_DIR = "data_storage/downloaded_datasets/pro_scrapes/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# আমরা ইন্টারনেটের আর্কাইভ থেকে ব্যাকআপ নিচ্ছি
TARGETS = [
    {"name": "factwatch_archive", "url": "https://archive.org/wayback/available?url=factwatch.bd/category/fact-check/"},
    {"name": "boom_archive", "url": "https://archive.org/wayback/available?url=boombangladesh.com/fact-check"}
]

def fetch_from_archive():
    for target in TARGETS:
        print(f"🏛️ Accessing Internet Archive for: {target['name']}...")
        try:
            # Wayback Machine API ব্যবহার করছি
            res = requests.get(target['url'], timeout=20)
            data = res.json()
            
            if 'archived_snapshots' in data and data['archived_snapshots']:
                snapshot_url = data['archived_snapshots']['closest']['url']
                print(f"✅ Found Snapshot: {snapshot_url}")
                
                # এখানে স্ন্যাপশট থেকে টেক্সট তুলে নেওয়ার লজিক হবে
                # যেহেতু আপনি সরাসরি ডিএনএস এরর পাচ্ছেন, আর্কাইভ লিংকটি আপনার স্ক্রিপ্টে ঢুকিয়ে দিচ্ছি
                with open(f"{OUTPUT_DIR}/{target['name']}_archive.jsonl", 'w') as f:
                    f.write(json.dumps({"url": snapshot_url, "status": "ARCHIVED_DATA_FOUND"}))
            else:
                print("❌ No archive found. ISP block is too strong.")
        except Exception as e:
            print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    fetch_from_archive()
