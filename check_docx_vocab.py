import docx

def check_vocab(filepath):
    try:
        doc = docx.Document(filepath)
        for p in doc.paragraphs:
            if "TỪ VỰNG" in p.text.upper() or "VOCAB" in p.text.upper():
                print(f"Found in {filepath}: {p.text.strip()}")
                return True
        print(f"No vocab found in {filepath}")
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

check_vocab('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx')
check_vocab('PART 03/SCRIPTS/LISTENING PART 03 - SCRIPTS.docx')
