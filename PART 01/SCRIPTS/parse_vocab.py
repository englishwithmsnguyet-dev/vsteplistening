import zipfile
import xml.etree.ElementTree as ET
import json
import re
import os

# Relative paths from the project root directory
docx_path = 'PART 01/SCRIPTS/LISTENING PART 01 - VOCAB.docx'
output_js = 'vocab_data.js'

if not os.path.exists(docx_path):
    print(f"Error: {docx_path} not found. Please make sure you are running this script from the project root directory.")
    exit(1)

print(f"Parsing {docx_path}...")

with zipfile.ZipFile(docx_path) as docx:
    xml_content = docx.read('word/document.xml')
    root = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    texts = []
    for p in root.findall('.//w:p', ns):
        p_text = []
        for r in p.findall('.//w:r', ns):
            t = r.find('.//w:t', ns)
            if t is not None and t.text:
                p_text.append(t.text)
        texts.append(''.join(p_text))

vocab_data = []
current_category = None
current_topic = None

# Main categories tracking
main_cats = {
    "📍 TỪ VỰNG LIÊN QUAN ĐẾN NGHỀ NGHIỆP/CHỨC VỤ": "Nghề nghiệp & Chức vụ",
    "📍 TỪ VỰNG LIÊN QUAN ĐẾN ĐỊA ĐIỂM": "Địa điểm & Bối cảnh",
    "🎉 MỘT SỐ SỰ KIỆN HAY XUẤT HIỆN": "Các sự kiện hay gặp"
}

for text in texts:
    cleaned = text.strip()
    if not cleaned:
        continue
    
    # Skip title lines
    if cleaned.startswith("PART 01:"):
        continue
        
    # Check if main category
    if cleaned in main_cats:
        current_category = {
            "name": main_cats[cleaned],
            "topics": []
        }
        vocab_data.append(current_category)
        current_topic = None
        continue
    
    # Check if subtopic
    is_subtopic = False
    emojis = ["🏫", "🧪", "🏥", "🏗️", "🎭", "⚖️", "🛠️", "📦", "🌍", "🍽️", "🏨", "🏦", "📮", "✈️", "🛍️", "🏬", "🏢", "🏠", "🚆", "🎉"]
    if any(cleaned.startswith(e) for e in emojis):
        is_subtopic = True
    elif not ("/" in cleaned or ":" in cleaned or "(" in cleaned):
        is_subtopic = True
        
    if is_subtopic:
        if current_category is None:
            current_category = {
                "name": "Từ vựng chung",
                "topics": []
            }
            vocab_data.append(current_category)
        
        # Clean subtopic name
        topic_name = cleaned
        for e in emojis:
            topic_name = topic_name.replace(e, "")
        topic_name = topic_name.strip()
        
        current_topic = {
            "name": topic_name,
            "words": []
        }
        current_category["topics"].append(current_topic)
        continue

    # Parse word item
    word_part = ""
    ipa_part = ""
    pos_part = ""
    meaning_part = ""
    
    match = re.match(r'([^\/]+)\s*\/([^\/]+)\/\s*(.*)', cleaned)
    if match:
        word_part = match.group(1).strip()
        ipa_part = f"/{match.group(2).strip()}/"
        remainder = match.group(3).strip()
        
        # Extract POS and meaning
        pos_match = re.match(r'\(([^)]+)\)\s*:\s*(.*)', remainder)
        if pos_match:
            pos_part = f"({pos_match.group(1).strip()})"
            meaning_part = pos_match.group(2).strip()
        else:
            meaning_part = remainder.replace(':', '').strip()
    else:
        # Format: word: meaning or word (pos): meaning
        colon_split = cleaned.split(':', 1)
        if len(colon_split) == 2:
            left = colon_split[0].strip()
            meaning_part = colon_split[1].strip()
            
            # Extract POS
            pos_match = re.search(r'\(([^)]+)\)', left)
            if pos_match:
                pos_part = f"({pos_match.group(1).strip()})"
                word_part = left.replace(pos_part, '').strip()
            else:
                word_part = left
        else:
            word_part = cleaned
            
    if word_part:
        if current_topic is None:
            if current_category is None:
                current_category = {"name": "Từ vựng chung", "topics": []}
                vocab_data.append(current_category)
            current_topic = {"name": "Từ vựng bổ sung", "words": []}
            current_category["topics"].append(current_topic)
            
        current_topic["words"].append({
            "word": word_part,
            "ipa": ipa_part,
            "pos": pos_part,
            "meaning": meaning_part
        })

# Write to vocab_data.js
js_content = "window.VSTEP_VOCAB_DATA = " + json.dumps(vocab_data, ensure_ascii=False, indent=2) + ";\n"
with open(output_js, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated {output_js} with {len(vocab_data)} categories.")
