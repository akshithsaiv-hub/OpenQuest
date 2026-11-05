import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "frontend", "data.js")

with open(data_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("UI_TRANSLATIONS = {")
if idx != -1:
    end_idx = content.find("};", idx) + 1
    sub = content[idx:end_idx]
    # Let's extract keys for 'en'
    en_idx = sub.find('"en":')
    next_lang_idx = sub.find('"te":')
    en_block = sub[en_idx:next_lang_idx]
    keys = re.findall(r'"([a-zA-Z0-9_]+)":', en_block)
    print("EN keys count:", len(keys))
    print("EN keys:", keys)
