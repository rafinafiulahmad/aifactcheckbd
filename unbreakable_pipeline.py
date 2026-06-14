import sqlite3
import json
import glob
import os

DB_FILE = "data_storage/factcheck_vault.db"
SCRAPE_DIR = "data_storage/downloaded_datasets/pro_scrapes/"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

def merge_new_data():
    files = glob.glob(f"{SCRAPE_DIR}/*.jsonl")
    for f_path in files:
        print(f"📂 Merging: {os.path.basename(f_path)}")
        with open(f_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO master_factcheck (data_id, claim_text, verdict, repo_source)
                        VALUES (?, ?, ?, ?)
                    ''', (str(os.urandom(16).hex()), data['claim_text'], data['verdict'], data['repo_source']))
                except: continue
    conn.commit()
    print("🏆 Merge Completed!")

if __name__ == "__main__":
    merge_new_data()
