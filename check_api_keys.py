import os
from dotenv import load_dotenv
load_dotenv()
import time, requests

GROQ_KEYS = [
    os.environ.get("GROQ_API_KEY_11"),
    os.environ.get("GROQ_API_KEY_12"),
    os.environ.get("GROQ_API_KEY_13"),
    os.environ.get("GROQ_API_KEY_14"),
    os.environ.get("GROQ_API_KEY_15"),
    os.environ.get("GROQ_API_KEY_16"),
    os.environ.get("GROQ_API_KEY_17"),
    os.environ.get("GROQ_API_KEY_18"),
    os.environ.get("GROQ_API_KEY_19"),
    os.environ.get("GROQ_API_KEY_20"),
]

def test_key(key, index):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code == 200: return "✅ WORKING"
        elif r.status_code == 429: return "⚠️  RATE LIMITED"
        elif r.status_code in [401,403]: return "🔴 INVALID KEY"
        else: return f"❓ ERROR {r.status_code}: {r.text[:80]}"
    except Exception as e:
        return f"💀 {str(e)[:50]}"

print("\n🔍 Testing all 10 Groq API keys...\n")
working = 0
for i, key in enumerate(GROQ_KEYS, 1):
    status = test_key(key, i)
    print(f"  Key {i:>2}: ...{key[-8:]}  →  {status}")
    if "WORKING" in status: working += 1
    time.sleep(1)
print(f"\n✅ Working: {working}/10  |  Capacity: ~{working*30} req/min\n")
