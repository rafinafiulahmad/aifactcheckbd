import asyncio
from playwright.async_api import async_playwright
import json
import os
import sys

# নিশ্চিত করা যে ডাটা স্টোরেজ রেডি আছে
OUTPUT_DIR = "data_storage/downloaded_datasets/pro_scrapes/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SITES = [
    {"name": "factwatch_bd", "url": "https://factwatch.bd/category/fact-check/", "selector": "h3"},
    {"name": "boom_bd", "url": "https://boombangladesh.com/fact-check", "selector": "h2"},
    {"name": "afp", "url": "https://factcheck.afp.com/", "selector": "h2"},
    {"name": "logically", "url": "https://www.logicallyfacts.com/en/fact-check", "selector": "h2"}
]

async def run_crawler():
    async with async_playwright() as p:
        # ব্রাউজার লঞ্চ - ডিবাগিং অপশনসহ
        browser = await p.chromium.launch(headless=True)
        
        for site in SITES:
            print(f"🔄 Processing: {site['name']}...")
            try:
                page = await browser.new_page()
                await page.goto(site['url'], timeout=60000, wait_until="domcontentloaded")
                await asyncio.sleep(3) # পেজ লোড হতে সময় দেওয়া
                
                titles = await page.eval_on_selector_all(site['selector'], "elements => elements.map(e => e.innerText)")
                
                if titles:
                    with open(f"{OUTPUT_DIR}/{site['name']}.jsonl", 'w', encoding='utf-8') as f:
                        for title in titles:
                            if len(title.strip()) > 10:
                                entry = {"claim_text": title.strip(), "verdict": "UNVERIFIED", "source": site['name']}
                                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    print(f"✅ Success: Saved {len(titles)} items from {site['name']}")
                else:
                    print(f"⚠️ No data found from {site['name']}")
                
                await page.close()
            except Exception as e:
                print(f"❌ Error in {site['name']}: {str(e)}")
        
        await browser.close()
        print("\n🚀 All tasks finished!")

if __name__ == "__main__":
    try:
        asyncio.run(run_crawler())
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
