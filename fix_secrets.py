import re

FILES = ["api_rotator.py", "check_api_keys.py", "unbreakable_factcheck_system.py", "unstoppable_pro_advanced.py"]
pattern = re.compile(r'["\']gsk_[A-Za-z0-9_\-]{20,}["\']')

env_lines = []
counter = 1
for fname in FILES:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()
    def repl(m):
        global counter
        key = m.group(0).strip("'\"")
        varname = f"GROQ_API_KEY_{counter}"
        env_lines.append(f"{varname}={key}")
        counter += 1
        return f'os.environ.get("{varname}")'
    new_content = pattern.sub(repl, content)
    if "import os" not in new_content:
        new_content = "import os\n" + new_content
    if "load_dotenv" not in new_content:
        new_content = new_content.replace("import os", "import os\nfrom dotenv import load_dotenv\nload_dotenv()", 1)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_content)

with open(".env", "w", encoding="utf-8") as f:
    f.write("\n".join(env_lines) + "\n")

print(f"Done. Replaced {counter-1} keys -> saved to .env")
