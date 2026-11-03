import json
import re

# Load extracted vocab for Practice 01
with open('extracted_practice_vocab.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

p1_vocab = vocab_data.get('01', [])

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the questions array of p1_practice_01 and inject the vocabulary.
# This requires parsing JS object. Since it's not strict JSON, it's safer to use regex or string manipulation.
# Let's find "p1_practice_01"
start_idx = content.find('"id": "p1_practice_01"')
end_idx = content.find('"id": "p1_practice_02"')

if start_idx != -1 and end_idx != -1:
    section = content[start_idx:end_idx]
    
    # We have 8 questions in Practice 01. p1_vocab has 7 items.
    # Wait, p1_vocab has 7 items, meaning one question didn't have a vocab block?
    # Let's match each question block and inject vocabulary before "options" or "transcript".
    
    # Find all "number": X
    question_blocks = []
    import re
    for m in re.finditer(r'"number":\s*\d+,', section):
        question_blocks.append(m.start())
        
    print(f"Found {len(question_blocks)} questions in Practice 01.")
    print(f"We have {len(p1_vocab)} vocab lists.")
    
    # I will just write a simpler JS patcher using python
    # For Practice 01:
    out_section = section
    for i in range(min(len(question_blocks), len(p1_vocab))):
        q_num = i + 1
        vocab_json = json.dumps(p1_vocab[i], ensure_ascii=False)
        # Find where to insert, right after "question_vi": "...",
        pattern = rf'("number":\s*{q_num},\s*.*?)(?=\n\s*"options")'
        
        def replacer(match):
            return match.group(1) + f'\n            "vocabulary": {vocab_json},'
            
        out_section = re.sub(pattern, replacer, out_section, flags=re.DOTALL)
        
    new_content = content[:start_idx] + out_section + content[end_idx:]
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched data.js for Practice 01 successfully.")
else:
    print("Could not find p1_practice_01")
