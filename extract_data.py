import json
import zipfile
import xml.etree.ElementTree as ET

with open('/Users/nguyetpham/Desktop/WEBSITE/LISTENING VSTEP/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

practices = ['p2_practice_05', 'p2_practice_06', 'p2_practice_07', 'p2_practice_08']
practice_questions = {}

def find_practices(obj):
    if isinstance(obj, dict):
        if obj.get('id') in practices:
            practice_questions[obj['id']] = [q['question'] for q in obj.get('questions', [])]
        for v in obj.values():
            find_practices(v)
    elif isinstance(obj, list):
        for item in obj:
            find_practices(item)

find_practices(data)
print("Question counts:", {k: len(v) for k, v in practice_questions.items()})

def read_docx_paragraphs(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = []
            for p in tree.findall('.//w:p', ns):
                texts = [node.text for node in p.findall('.//w:t', ns) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return paragraphs
    except Exception as e:
        return [str(e)]

paragraphs = read_docx_paragraphs('/Users/nguyetpham/Desktop/WEBSITE/LISTENING VSTEP/PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx')
practice_texts = {}
current_p = None

for p in paragraphs:
    if "PRACTICE 05" in p.upper() or "PRACTICE 5" in p.upper() and "PRACTICE 05" not in p.upper():
        if "PRACTICE 05" in p.upper():
            current_p = 'p2_practice_05'
            practice_texts[current_p] = []
    elif "PRACTICE 06" in p.upper():
        current_p = 'p2_practice_06'
        practice_texts[current_p] = []
    elif "PRACTICE 07" in p.upper():
        current_p = 'p2_practice_07'
        practice_texts[current_p] = []
    elif "PRACTICE 8" in p.upper() or "PRACTICE 08" in p.upper():
        current_p = 'p2_practice_08'
        practice_texts[current_p] = []
    elif "PRACTICE" in p.upper() and current_p:
        if "09" in p.upper() or "9" in p.upper():
            current_p = None
    
    if current_p:
        practice_texts[current_p].append(p)

with open('extracted_output.txt', 'w', encoding='utf-8') as f:
    for p_id in practices:
        f.write(f"--- {p_id} ---\n")
        f.write("Questions:\n")
        for i, q in enumerate(practice_questions.get(p_id, [])):
            f.write(f"{i+1}: {q}\n")
        f.write("\nTranscript:\n")
        f.write("\n".join(practice_texts.get(p_id, [])))
        f.write("\n==================================\n\n")
