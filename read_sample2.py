import docx

def read_sample(filepath, start_line, end_line):
    print(f"--- {filepath} ---")
    try:
        doc = docx.Document(filepath)
        for i, p in enumerate(doc.paragraphs):
            if i < start_line:
                continue
            text = p.text.strip()
            if text:
                print(text)
            if i >= end_line:
                break
    except Exception as e:
        print(f"Error: {e}")

read_sample('PART 02/SCRIPTS/SCRIPTS B2 - PART 02.docx', 31, 80)
