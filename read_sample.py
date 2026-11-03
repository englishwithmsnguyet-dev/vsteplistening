import docx

def read_sample(filepath, lines):
    print(f"--- {filepath} ---")
    try:
        doc = docx.Document(filepath)
        for i, p in enumerate(doc.paragraphs):
            text = p.text.strip()
            if text:
                print(text)
            if i > lines:
                break
    except Exception as e:
        print(f"Error: {e}")

read_sample('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx', 30)
