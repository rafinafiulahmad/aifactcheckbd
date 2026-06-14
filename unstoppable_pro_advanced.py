import sqlite3
import random
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Task, Crew

# আপনার ১১টি API Key
GROQ_KEYS = [
    os.environ.get("GROQ_API_KEY_31"),
    os.environ.get("GROQ_API_KEY_32"),
    os.environ.get("GROQ_API_KEY_33"),
    os.environ.get("GROQ_API_KEY_34"),
    os.environ.get("GROQ_API_KEY_35"),
    os.environ.get("GROQ_API_KEY_36"),
    os.environ.get("GROQ_API_KEY_37"),
    os.environ.get("GROQ_API_KEY_38"),
    os.environ.get("GROQ_API_KEY_39"),
    os.environ.get("GROQ_API_KEY_40")
]

# এনভায়রনমেন্ট ভেরিয়েবল সেট করা (লেটেস্ট CrewAI এর জন্য জরুরি)
os.environ["GROQ_API_KEY"] = random.choice(GROQ_KEYS)

def start_verification():
    db_path = "data_storage/factcheck_vault.db"
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # ডাটাবেজ থেকে রেন্ডম একটি ডাটা নেওয়া
    cursor.execute("SELECT claim_text FROM master_factcheck ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        print("⚠️ Database is empty.")
        return
        
    claim = row[0]
    print(f"🔍 Analyzing: {claim}")

    # এজেন্ট তৈরি
    checker = Agent(
        role='Fact Checker',
        goal='Identify fake news',
        backstory='Expert analyst for news verification.',
        llm="groq/llama3-70b-8192"
    )

    # টাস্ক সেটআপ
    task = Task(
        description=f"Analyze this claim: '{claim}'. Provide a verdict (True/False/Misleading) and logic.",
        expected_output='A professional verdict report.'
    )

    # ক্রু রান
    crew = Crew(agents=[checker], tasks=[task])
    print("\n🚀 Agent is processing...")
    print(crew.kickoff())
    conn.close()

if __name__ == "__main__":
    start_verification()
