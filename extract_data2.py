import json
import zipfile
import xml.etree.ElementTree as ET

# Load data.json
with open('/Users/nguyetpham/Desktop/WEBSITE/LISTENING VSTEP/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

practices = ['p2_practice_05', 'p2_practice_06', 'p2_practice_07', 'p2_practice_08']
counts = {}
practice_questions = {}

for item in data:
    if item.get('id') in practices:
        counts[item['id']] = len(item.get('questions', []))
        practice_questions[item['id']] = [q['question'] for q in item.get('questions', [])]

print("Question counts:", counts)

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
    if "PRACTICE 05" in p.upper():
        current_p = 'p2_practice_05'
        practice_texts[current_p] = []
    elif "PRACTICE 06" in p.upper():
        current_p = 'p2_practice_06'
        practice_texts[current_p] = []
    elif "PRACTICE 07" in p.upper():
        current_p = 'p2_practice_07'
        practice_texts[current_p] = []
    elif "PRACTICE 8" in p.upper():
        current_p = 'p2_practice_08'
        practice_texts[current_p] = []
    elif "PRACTICE" in p.upper() and current_p:
        pass # another practice
    
    if current_p:
        practice_texts[current_p].append(p)

for p_id in practices:
    print(f"--- {p_id} ---")
    print("Questions:")
    for i, q in enumerate(practice_questions[p_id]):
        print(f"{i+1}: {q}")
    print("\nTranscript:")
    print("\n".join(practice_texts.get(p_id, [])))
    print("==================================\n")
