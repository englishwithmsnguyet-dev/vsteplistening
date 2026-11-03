import docx

doc = docx.Document('PART 01/SCRIPTS/VSTEP LISTENING PART 1 - TRANSCRIPT.docx')
for i, p in enumerate(doc.paragraphs):
    if 'PRACTICE' in p.text.upper():
        print(f"[{i}] {p.text.strip()}")
