import docx
import json
import re

def is_vietnamese(text):
    vietnamese_chars = set('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')
    for char in text:
        if char in vietnamese_chars:
            return True
    return False

def parse_docx(filepath, prefix):
    doc = docx.Document(filepath)
    practices = {}
    current_practice = None
    transcript_lines = []
    
    in_transcript = False
    
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text: continue
        
        # Detect practice header
        match = re.match(r'^(?:PRACTICE|TEST)\s*0?(\d+)', text, re.IGNORECASE)
        if match:
            # Save previous
            if current_practice and transcript_lines:
                # split into EN and VI
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
                        
                practices[current_practice] = {
                    'en_transcript': en_lines,
                    'vi_transcript': vi_lines
                }
            
            p_num = int(match.group(1))
            current_practice = f"{prefix}_practice_{str(p_num).zfill(2)}"
            transcript_lines = []
            in_transcript = False
            continue
            
        if current_practice:
            if text.upper() == "TRANSCRIPTS" or text.upper() == "TRANSCRIPT":
                in_transcript = True
                continue
            
            if in_transcript:
                # Add to transcript lines
                transcript_lines.append(text)
                
    # Save the last one
    if current_practice and transcript_lines:
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
                
        practices[current_practice] = {
            'en_transcript': en_lines,
            'vi_transcript': vi_lines
        }
        
    return practices

all_practices = {}
all_practices.update(parse_docx('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx', 'p2'))
all_practices.update(parse_docx('PART 03/SCRIPTS/LISTENING PART 03 - SCRIPTS.docx', 'p3'))

# Debug print
for k, v in all_practices.items():
    print(f"{k}: {len(v['en_transcript'])} EN lines, {len(v['vi_transcript'])} VI lines")

# Patch data.js
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

for pid, trans in all_practices.items():
    start_idx = content.find(f'"id": "{pid}"')
    if start_idx == -1:
        continue
        
    # Find the end of this practice
    next_idx = content.find('"id": "p', start_idx + 100)
    end_idx = next_idx if next_idx != -1 else len(content)
    
    section = content[start_idx:end_idx]
    
    # Insert before "questions": [
    q_start = section.find('"questions":')
    if q_start != -1:
        en_json = json.dumps(trans['en_transcript'], ensure_ascii=False)
        vi_json = json.dumps(trans['vi_transcript'], ensure_ascii=False)
        
        insert_str = f'"en_transcript": {en_json},\n        "vi_transcript": {vi_json},\n        '
        section = section[:q_start] + insert_str + section[q_start:]
        
    content = content[:start_idx] + section + content[end_idx:]

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("data.js patched successfully!")
