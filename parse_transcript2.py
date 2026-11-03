import docx

doc = docx.Document('PART 01/SCRIPTS/VSTEP LISTENING PART 1 - TRANSCRIPT.docx')
for i, p in enumerate(doc.paragraphs[267:300]):
    print(f"[{i}] {p.text.strip()}")
