import docx

doc = docx.Document('PART 01/SCRIPTS/LISTENING PART 01 - VOCAB.docx')
for p in doc.paragraphs:
    if p.text.strip().startswith('PRACTICE') or p.text.strip().startswith('DẠNG'):
        print(p.text.strip())
