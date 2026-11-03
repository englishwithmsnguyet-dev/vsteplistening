import docx

doc = docx.Document('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx')
printing = False
for p in doc.paragraphs:
    text = p.text.strip()
    if not text: continue
    if text.upper() == "PRACTICE 8":
        printing = True
    if printing:
        print(text)
