import json
import re

# Load all vocab files
vocab_data = {}

def load_vocab(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            vocab_data.update(data)
    except Exception as e:
        print(f"Error loading {filename}: {e}")

load_vocab('vocab_p2_1.json')
load_vocab('vocab_p2_2.json')
load_vocab('vocab_p3.json')

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# For each practice test ID in vocab_data, find its section and inject the vocabulary arrays
for pid, vocab_lists in vocab_data.items():
    print(f"Patching {pid} with {len(vocab_lists)} questions.")
    
    start_idx = content.find(f'"id": "{pid}"')
    if start_idx == -1:
        print(f"  Warning: {pid} not found in data.js")
        continue
    
    # Find the end of this practice section
    # Next practice might be p2_ or p3_ or end of file
    next_idx = content.find('"id": "p', start_idx + 100)
    if next_idx == -1:
        end_idx = len(content)
    else:
        end_idx = next_idx
        
    section = content[start_idx:end_idx]
    
    # Find all question blocks
    question_blocks = []
    for m in re.finditer(r'"number":\s*\d+,', section):
        question_blocks.append(m.start())
        
    if len(question_blocks) != len(vocab_lists):
        print(f"  Warning: Question count mismatch for {pid}. Found {len(question_blocks)}, have {len(vocab_lists)} vocab lists.")
    
    out_section = section
    for i in range(min(len(question_blocks), len(vocab_lists))):
        q_num = i + 1
        vocab_json = json.dumps(vocab_lists[i], ensure_ascii=False)
        # Find where to insert, right after "question_vi": "..." or "question": "..."
        # Note: some questions might not have question_vi. It's safer to insert before "options"
        pattern = rf'("number":\s*{q_num},\s*.*?)(?=\n\s*"options")'
        
        def replacer(match):
            return match.group(1) + f'\n            "vocabulary": {vocab_json},'
            
        out_section = re.sub(pattern, replacer, out_section, flags=re.DOTALL)
        
    content = content[:start_idx] + out_section + content[end_idx:]

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patching complete!")
