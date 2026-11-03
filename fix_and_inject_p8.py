import docx
import json
import re

def is_vietnamese(text):
    vietnamese_chars = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')
    for char in text:
        if char in vietnamese_chars:
            return True
    return False

doc = docx.Document('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx')
printing = False
in_transcript = False
transcript_lines = []

for p in doc.paragraphs:
    text = p.text.strip()
    if not text: continue
    
    if text.upper() == "PRACTICE 8":
        printing = True
    elif text.upper().startswith("PRACTICE") and "8" not in text and printing:
        break
        
    if printing:
        if text.upper() == "TRANSCRIPTS" or text.upper() == "TRANSCRIPT":
            in_transcript = True
            continue
        if in_transcript:
            transcript_lines.append(text)

en_lines = []
vi_lines = []
found_vi = False
for line in transcript_lines:
    if not found_vi and is_vietnamese(line):
        found_vi = True
    if found_vi:
        vi_lines.append(line)
    else:
        en_lines.append(line)

print(f"p2_practice_08: {len(en_lines)} EN lines, {len(vi_lines)} VI lines")

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

pid = "p2_practice_08"
start_idx = content.find(f'"id": "{pid}"')
next_idx = content.find('"id": "p', start_idx + 100)
end_idx = next_idx if next_idx != -1 else len(content)

section = content[start_idx:end_idx]

# Replace existing en_transcript and vi_transcript arrays
section = re.sub(r'"en_transcript": \[.*?\],\s*', '', section, flags=re.DOTALL)
section = re.sub(r'"vi_transcript": \[.*?\],\s*', '', section, flags=re.DOTALL)

q_start = section.find('"questions":')
if q_start != -1:
    en_json = json.dumps(en_lines, ensure_ascii=False)
    vi_json = json.dumps(vi_lines, ensure_ascii=False)
    
    insert_str = f'"en_transcript": {en_json},\n        "vi_transcript": {vi_json},\n        '
    section = section[:q_start] + insert_str + section[q_start:]
    
content = content[:start_idx] + section + content[end_idx:]

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(content)

