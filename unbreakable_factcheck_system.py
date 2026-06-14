import os
from dotenv import load_dotenv
load_dotenv()
import sqlite3, random, os, time, json, logging, requests
from datetime import datetime
from itertools import cycle

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("factcheck_log.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

GROQ_KEYS = [
    os.environ.get("GROQ_API_KEY_21"),
    os.environ.get("GROQ_API_KEY_22"),
    os.environ.get("GROQ_API_KEY_23"),
    os.environ.get("GROQ_API_KEY_24"),
    os.environ.get("GROQ_API_KEY_25"),
    os.environ.get("GROQ_API_KEY_26"),
    os.environ.get("GROQ_API_KEY_27"),
    os.environ.get("GROQ_API_KEY_28"),
    os.environ.get("GROQ_API_KEY_29"),
    os.environ.get("GROQ_API_KEY_30"),
]

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "qwen/qwen3-32b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

# ── API ROTATOR ──────────────────────────────────────
class APIRotator:
    def __init__(self, keys, models):
        self.keys = keys
        self.models = models
        self._key_cycle = cycle(keys)
        self._model_cycle = cycle(models)
        self.cooldowns = {}
        self.fail_counts = {k: 0 for k in keys}
        self.current_key = next(self._key_cycle)
        self.current_model = models[0]

    def rotate(self, failed_key=None, cooldown_sec=60):
        if failed_key:
            self.cooldowns[failed_key] = time.time() + cooldown_sec
            self.fail_counts[failed_key] += 1
            log.warning(f"🔴 Key ...{failed_key[-8:]} cooldown {cooldown_sec}s")
        # find next available key
        for _ in range(len(self.keys) * 2):
            key = next(self._key_cycle)
            if time.time() > self.cooldowns.get(key, 0):
                self.current_key = key
                break
        self.current_model = next(self._model_cycle)
        log.info(f"🔑 Now using: ...{self.current_key[-8:]} | {self.current_model}")

rotator = APIRotator(GROQ_KEYS, GROQ_MODELS)

# ── DIRECT GROQ API CALL (no CrewAI/LiteLLM cache issue) ──
def groq_call(messages: list, model: str, key: str, max_tokens=1500) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ── 3-AGENT PIPELINE (manual, no CrewAI bug) ─────────
def run_agent_pipeline(claim: str, model: str, key: str) -> str:

    # Agent 1: Researcher
    log.info("🔎 Agent 1: Researcher...")
    research = groq_call([
        {"role": "user", "content": (
            f"You are a senior research analyst. Research this claim and list the key facts, "
            f"entities, dates, and what needs verification:\n\nCLAIM: '{claim}'\n\n"
            f"Give a structured bullet-point analysis."
        )}
    ], model, key)

    # Agent 2: Fact Checker
    log.info("⚖️  Agent 2: Fact Checker...")
    verdict = groq_call([
        {"role": "user", "content": (
            f"You are an expert fact-checker. Based on this research:\n{research}\n\n"
            f"Now fact-check this claim: '{claim}'\n\n"
            f"Give: VERDICT (TRUE/FALSE/MISLEADING/UNVERIFIABLE), "
            f"CONFIDENCE (0-100%), and your REASONING."
        )}
    ], model, key)

    # Agent 3: Report Writer
    log.info("📝 Agent 3: Report Writer...")
    report = groq_call([
        {"role": "user", "content": (
            f"You are a fact-check report writer. Write a professional report:\n\n"
            f"Research findings: {research}\n\n"
            f"Fact-check verdict: {verdict}\n\n"
            f"Format the final report EXACTLY like this:\n"
            f"📋 CLAIM: {claim}\n"
            f"⚖️ VERDICT: [TRUE/FALSE/MISLEADING/UNVERIFIABLE]\n"
            f"📊 CONFIDENCE: [0-100%]\n"
            f"🔍 ANALYSIS: [2-3 sentences]\n"
            f"📌 CONCLUSION: [1 sentence summary]"
        )}
    ], model, key)

    return report

# ── DATA LOADER ───────────────────────────────────────
DB_PATH = "data_storage/factcheck_vault.db"
RESULTS_FILE = "factcheck_results.jsonl"

def get_claim():
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cur.fetchall()]
            for table in tables:
                try:
                    cur.execute(f"SELECT * FROM {table} ORDER BY RANDOM() LIMIT 1")
                    row = cur.fetchone()
                    if row:
                        texts = [str(r) for r in row if r and len(str(r)) > 20]
                        if texts:
                            conn.close()
                            return max(texts, key=len)
                except:
                    continue
            conn.close()
        except Exception as e:
            log.error(f"DB error: {e}")
    return "বাংলাদেশে ডিজিটাল সাক্ষরতার হার উল্লেখযোগ্যভাবে বৃদ্ধি পেয়েছে।"

def save_result(claim, verdict, model, key_suffix):
    record = {
        "timestamp": datetime.now().isoformat(),
        "claim": claim[:500],
        "verdict": str(verdict)[:3000],
        "model": model,
        "key": key_suffix,
    }
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    log.info(f"💾 Saved to {RESULTS_FILE}")

# ── MAIN RUNNER WITH AUTO-RETRY ───────────────────────
def run_check(claim=None, max_retries=10):
    if not claim:
        claim = get_claim()

    print(f"\n{'='*60}")
    print(f"🔍 CLAIM: {claim[:150]}")
    print(f"{'='*60}")

    for attempt in range(1, max_retries + 1):
        key = rotator.current_key
        model = rotator.current_model
        log.info(f"🚀 Attempt {attempt}/{max_retries} | {model} | ...{key[-8:]}")

        try:
            result = run_agent_pipeline(claim, model, key)
            save_result(claim, result, model, key[-8:])
            print(f"\n✅ FACT-CHECK COMPLETE\n{'='*60}")
            print(result)
            print(f"{'='*60}\n")
            return result

        except requests.exceptions.HTTPError as e:
            code = e.response.status_code if e.response else 0
            log.error(f"❌ HTTP {code}: {str(e)[:100]}")
            if code == 429:
                rotator.rotate(failed_key=key, cooldown_sec=90)
            elif code in [401, 403]:
                rotator.rotate(failed_key=key, cooldown_sec=99999)
            else:
                rotator.rotate(failed_key=key, cooldown_sec=15)

        except Exception as e:
            log.error(f"❌ Error: {str(e)[:150]}")
            rotator.rotate(cooldown_sec=10)

        wait = min(5 * attempt, 30)
        log.info(f"⏳ Waiting {wait}s before retry...")
        time.sleep(wait)

    log.error("💀 All retries exhausted.")
    return None

# ── ENTRY POINT ───────────────────────────────────────
if __name__ == "__main__":
    import sys
    print("""
╔══════════════════════════════════════════════════╗
║   UNBREAKABLE FACT-CHECK SYSTEM v4.0           ║
║   Direct Groq API | No CrewAI cache bug        ║
║   10 Keys | 4 Models | Auto-Rotation           ║
╚══════════════════════════════════════════════════╝
    """)

    if len(sys.argv) >= 2:
        if sys.argv[1] == "batch":
            count = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
            for i in range(count):
                print(f"\n📌 [{i+1}/{count}]")
                run_check()
                time.sleep(3)
        else:
            run_check(" ".join(sys.argv[1:]))
    else:
        run_check()
