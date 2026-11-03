import re

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def check_vocab(part_id_prefix):
    # Find all objects with an id starting with part_id_prefix
    # e.g. "id": "p2_practice_01"
    matches = list(re.finditer(rf'"id":\s*"{part_id_prefix}[^"]*"', content))
    
    total_questions = 0
    vocab_count = 0
    
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        section = content[start:end]
        
        # count questions
        total_questions += section.count('"question":')
        # count vocabularies
        vocab_count += section.count('"vocabulary":')
        
    return total_questions, vocab_count

q2, v2 = check_vocab('p2_')
q3, v3 = check_vocab('p3_')

print(f"PART 2: {q2} questions found, {v2} have vocabulary.")
print(f"PART 3: {q3} questions found, {v3} have vocabulary.")
