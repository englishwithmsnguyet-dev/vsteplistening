import docx

doc = docx.Document('PART 01/SCRIPTS/VSTEP LISTENING PART 1 - TRANSCRIPT.docx')
for i, p in enumerate(doc.paragraphs[450:475]):
    print(f"[{i+450}] {p.text.strip()}")
