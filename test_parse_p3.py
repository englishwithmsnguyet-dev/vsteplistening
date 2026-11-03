import docx

doc = docx.Document('PART 03/SCRIPTS/LISTENING PART 03 - SCRIPTS.docx')
printing = False
for p in doc.paragraphs:
    text = p.text.strip()
    if not text: continue
    if "PRACTICE" in text.upper() and "01" in text:
        printing = True
    elif "PRACTICE" in text.upper() and "02" in text:
        break
        
    if printing:
        print(text)
