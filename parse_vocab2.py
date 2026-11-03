import docx

doc = docx.Document('PART 01/SCRIPTS/LISTENING PART 01 - VOCAB.docx')
for i, p in enumerate(doc.paragraphs[:30]):
    print(f"[{i}] {p.text.strip()}")
