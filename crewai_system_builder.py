import os
import random
from crewai import Agent, Task, Crew, Process

# ১১টি Groq API Key এর লিস্ট
GROQ_KEYS = ["gsk_key1...", "gsk_key2...", "..."] # আপনার ১১টি কী এখানে বসান

def get_random_key():
    return random.choice(GROQ_KEYS)

# ১. এজেন্ট ডিফাইন করা
fact_checker = Agent(
    role='Lead Fact Checker',
    goal='Verify claims against the master database',
    backstory='You are an expert at analyzing 800k+ data points.',
    llm=f"groq/llama3-70b-8192", # Groq ব্যবহার করবে
    api_key=get_random_key()
)

# ২. টাস্ক ডিফাইন করা
verification_task = Task(
    description='Analyze new claims and cross-reference with database',
    expected_output='Verified fact reports',
    agent=fact_checker
)

# ৩. ক্রু বিল্ড করা
fact_crew = Crew(
    agents=[fact_checker],
    tasks=[verification_task],
    process=Process.sequential
)

def run_system():
    print("🚀 Building and Running Autonomous Fact-Checking System...")
    result = fact_crew.kickoff()
    print(result)

if __name__ == "__main__":
    run_system()
