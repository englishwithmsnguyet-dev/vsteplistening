import json
import re

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def get_transcripts(practice_id):
    start = content.find(f'"id": "{practice_id}"')
    if start == -1: return []
    end = content.find('"id": "p1_practice_', start + 100)
    if end == -1: end = content.find('"id": "p2_', start + 100)
    section = content[start:end]
    
    transcripts = []
    # Find all "transcript": "..."
    for m in re.finditer(r'"transcript":\s*"(.*?)"', section):
        transcripts.append(m.group(1))
    return transcripts

for pid in ['p1_practice_02', 'p1_practice_03', 'p1_practice_04']:
    ts = get_transcripts(pid)
    print(f"--- {pid} ---")
    for i, t in enumerate(ts):
        print(f"Q{i+1}: {t[:100]}...")
