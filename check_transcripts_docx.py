import docx

def list_headings(filepath):
    print(f"--- {filepath} ---")
    try:
        doc = docx.Document(filepath)
        for p in doc.paragraphs:
            if "PRACTICE" in p.text.upper() or "TEST" in p.text.upper():
                print(p.text.strip())
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

list_headings('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx')
list_headings('PART 03/SCRIPTS/LISTENING PART 03 - SCRIPTS.docx')
