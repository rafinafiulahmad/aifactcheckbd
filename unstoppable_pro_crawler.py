import asyncio
from playwright.async_api import async_playwright
import json
import os

OUTPUT_DIR = "data_storage/downloaded_datasets/pro_scrapes/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ১০টি সাইটের সিলেক্টর এবং ইউআরএল কনফিগারেশন
SITES = [
    {"name": "factwatch_bd", "url": "https://factwatch.bd/category/fact-check/", "selector": "h3"},
    {"name": "boomlive_in", "url": "https://www.boomlive.in/fact-check", "selector": ".card-title"},
    {"name": "altnews_in", "url": "https://www.altnews.in/category/fact-check/", "selector": ".entry-title"},
    {"name": "prothomalo", "url": "https://www.prothomalo.com/topic/fact-check", "selector": "h2"},
    {"name": "daily_star_bd", "url": "https://www.thedailystar.net/topic/fact-check", "selector": "h3"},
    {"name": "afp_factcheck", "url": "https://factcheck.afp.com/", "selector": "h2"},
    {"name": "vishvas_news", "url": "https://www.vishvasnews.com/fact-check/", "selector": ".card-title"},
    {"name": "logically_facts", "url": "https://www.logicallyfacts.com/en/fact-check", "selector": "h2"},
    {"name": "newsmobile_fc", "url": "https://newsmobile.in/articles/category/fact-check/", "selector": ".entry-title"},
    {"name": "quill_factcheck", "url": "https://www.thequint.com/news/webqoof", "selector": "h2"}
]

async def scrape_site(page, site):
    print(f"🔄 Scraping {site['name']}...")
    try:
        await page.goto(site['url'], wait_until="domcontentloaded", timeout=60000)
        # নির্দিষ্ট সময়ের জন্য ওয়েট করা যাতে জাভাস্ক্রিপ্ট লোড হতে পারে
        await asyncio.sleep(3) 
        
        items = await page.query_selector_all(site['selector'])
        data_list = []
        
        for item in items:
            title = await item.inner_text()
            if len(title.strip()) > 10: # খালি বা ছোট লাইন বাদ দেওয়া
                data = {
                    "claim_text": title.strip(),
                    "verdict": "UNVERIFIED",
                    "evidence_text": "Scraped via Playwright Pro",
                    "repo_source": site['name'],
                    "url": site['url']
                }
                data_list.append(data)
        
        with open(f"{OUTPUT_DIR}/{site['name']}.jsonl", 'w', encoding='utf-8') as f:
            for entry in data_list:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        print(f"✅ Saved {len(data_list)} records from {site['name']}")
    except Exception as e:
        print(f"❌ Failed {site['name']}: {e}")

async def main():
    async with async_playwright() as p:
        # ব্রাউজার লঞ্চ - ইউজার এজেন্ট সেট করা যাতে সাইটগুলো ব্লক না করে
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = await context.new_page()
        
        for site in SITES:
            await scrape_site(page, site)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
