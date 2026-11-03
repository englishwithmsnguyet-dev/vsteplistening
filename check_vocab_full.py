import docx
doc = docx.Document('PART 01/SCRIPTS/LISTENING PART 01 - VOCAB.docx')
found = False
for p in doc.paragraphs:
    if 'PRACTICE' in p.text.upper() or 'LUYỆN TẬP' in p.text.upper():
        print("Found:", p.text.strip())
        found = True
if not found:
    print("Not found anything related to Practice.")
