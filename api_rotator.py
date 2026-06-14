import os
from dotenv import load_dotenv
load_dotenv()
from crewai import LLM

class UnbreakableLLMManager:
    def __init__(self):
        self.current_index = 0
        self.keys = [
            os.environ.get("GROQ_API_KEY_1"),
            os.environ.get("GROQ_API_KEY_2"),
            os.environ.get("GROQ_API_KEY_3"),
            os.environ.get("GROQ_API_KEY_4"),
            os.environ.get("GROQ_API_KEY_5"),
            os.environ.get("GROQ_API_KEY_6"),
            os.environ.get("GROQ_API_KEY_7"),
            os.environ.get("GROQ_API_KEY_8"),
            os.environ.get("GROQ_API_KEY_9"),
            os.environ.get("GROQ_API_KEY_10")
        ]
        print(f"✅ [API ROTATOR] সফলভাবে {len(self.keys)}টি ওয়ান-টাইম Groq API Key ইঞ্জিনে লোড করা হয়েছে।")

    def get_robust_llm(self):
        """বর্তমান সচল এপিআই কী দিয়ে LLM অবজেক্ট রিটার্ন করে"""
        active_key = self.keys[self.current_index]
        print(f"🔑 [API ACTIVE] বর্তমানে Groq Key Index: {self.current_index + 1} ব্যবহার করা হচ্ছে।")
        
        # এখানে cache_prompt=False ডিফাইন করে এররটি ব্লক করা হলো
        return LLM(
            model="groq/llama3-70b-8192",
            api_key=active_key,
            temperature=0.1,
            cache_prompt=False
        )

    def rotate_key(self):
        """কোনো কি রেট লিমিট বা ফেইলর খেলে স্বয়ংক্রিয়ভাবে পরের কী-তে জাম্প করে"""
        if len(self.keys) > 1:
            self.current_index = (self.current_index + 1) % len(self.keys)
            print(f"🔄 [ALERT] API Limit/Failure! Switched to Groq Key Index: {self.current_index + 1}")
        else:
            print("⚠️ [WARNING] ব্যাকআপে আর কোনো API Key অবশিষ্ট নেই!")
