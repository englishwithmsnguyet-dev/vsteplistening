import re

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def count_transcripts(part_id_prefix):
    matches = list(re.finditer(rf'"id":\s*"{part_id_prefix}[^"]*"', content))
    t_count = 0
    q_count = 0
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        section = content[start:end]
        t_count += section.count('"transcript":')
        q_count += section.count('"question":')
    return q_count, t_count

q2, t2 = count_transcripts('p2_')
q3, t3 = count_transcripts('p3_')

print(f"PART 2: {q2} questions, {t2} transcripts.")
print(f"PART 3: {q3} questions, {t3} transcripts.")
