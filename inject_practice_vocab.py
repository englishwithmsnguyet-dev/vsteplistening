import docx
import re
import json

doc = docx.Document('PART 01/SCRIPTS/VSTEP LISTENING PART 1 - TRANSCRIPT.docx')

current_practice = None
question_index = -1
in_vocab = False
vocab_list = []

practice_data = {
    '01': [], '02': [], '03': [], '04': []
}

for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue
        
    m = re.match(r'^PRACTICE (0[1-4])$', text, re.IGNORECASE)
    if m:
        current_practice = m.group(1)
        question_index = -1
        in_vocab = False
        continue
        
    if current_practice and "TỪ VỰNG HỮU ÍCH" in text:
        in_vocab = True
        question_index += 1
        practice_data[current_practice].append([])
        continue
        
    if in_vocab:
        # Check if we hit the transcript or next question
        if "Tiếng Anh" in text or "Tiếng Việt" in text or re.match(r'^Câu \d+:', text) or "Question" in text:
            in_vocab = False
            continue
        
        # It's a vocab item
        practice_data[current_practice][question_index].append(text)

# Now we need to read data.js, find the questions array for each p1_practice_XX, and inject the vocabulary array
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We will use simple string replacement
# The structure in data.js is like:
# "id": "p1_practice_01",
# "title": "...",
# "questions": [
#     {
#         "options": [...],
#         "transcript": ...
#     }
# ]
# We will parse the JS file as a string, but it's risky. Let's output JSON first to see if extraction worked.

with open('extracted_practice_vocab.json', 'w', encoding='utf-8') as f:
    json.dump(practice_data, f, ensure_ascii=False, indent=2)

print("Extraction complete. Check extracted_practice_vocab.json")
