import docx

doc = docx.Document('PART 01/SCRIPTS/VSTEP LISTENING PART 1 - TRANSCRIPT.docx')
for i, p in enumerate(doc.paragraphs[450:500]):
    text = p.text.strip()
    if text:
        print(f"[{i+450}] {text}")
