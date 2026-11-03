import re, json

with open('scratch/mock_test_docx_text.txt', encoding='utf-8') as f:
    raw_lines = [l.strip() for l in f if l.strip()]

# Let's inspect the sections
# 1. Part 1 (Questions 1 - 8)
# In Part 1, each question has:
# EN Q, EN Options (A-D), EN Transcript
# VI Q, VI Options (A-D with checkmark), VI Transcript

part1_questions = []
# Answers from verified list:
answers_p1 = {1: 'D', 2: 'C', 3: 'B', 4: 'C', 5: 'D', 6: 'A', 7: 'B', 8: 'B'}

# Let's find each question block in Part 1 (indices 2 to 109)
p1_lines = raw_lines[1:110]

# Helper to parse Part 1
def parse_part1(lines):
    questions = []
    # Loop for q 1 to 8
    # For question i, find where "i. " begins in EN and VI
    for q_num in range(1, 9):
        # find EN question index
        en_idx = None
        vi_idx = None
        for idx, l in enumerate(lines):
            if re.match(rf'^{q_num}\.\s+', l):
                if en_idx is None:
                    en_idx = idx
                else:
                    vi_idx = idx
                    break
        
        # Next question start index
        next_en_idx = None
        if q_num < 8:
            for idx, l in enumerate(lines):
                if re.match(rf'^{q_num+1}\.\s+', l):
                    next_en_idx = idx
                    break
        else:
            next_en_idx = len(lines)
            
        # Slice lines for this question
        # between en_idx and vi_idx is EN part
        en_block = lines[en_idx:vi_idx]
        # between vi_idx and next_en_idx is VI part
        vi_block = lines[vi_idx:next_en_idx]
        
        en_q_text = re.sub(rf'^{q_num}\.\s+', '', en_block[0]).strip()
        # EN options
        en_opts = []
        en_transcript_lines = []
        for l in en_block[1:]:
            m = re.match(r'^([A-D])\.\s+(.*)$', l)
            if m and len(en_opts) < 4:
                en_opts.append({'letter': m.group(1), 'text': m.group(2).strip()})
            else:
                en_transcript_lines.append(l)
                
        vi_q_text = re.sub(rf'^{q_num}\.\s+', '', vi_block[0]).strip()
        vi_opts = []
        vi_transcript_lines = []
        correct_letter = answers_p1[q_num]
        for l in vi_block[1:]:
            m = re.match(r'^([A-D])\.\s+(.*)$', l)
            if m and len(vi_opts) < 4:
                opt_text = m.group(2).strip()
                if '✅' in opt_text:
                    correct_letter = m.group(1)
                    opt_text = opt_text.replace('✅', '').strip()
                vi_opts.append({'letter': m.group(1), 'text_vi': opt_text})
            else:
                vi_transcript_lines.append(l)
                
        # Merge options
        combined_opts = []
        for i in range(4):
            letter = chr(65 + i)
            e_text = en_opts[i]['text'] if i < len(en_opts) else ''
            v_text = vi_opts[i]['text_vi'] if i < len(vi_opts) else ''
            combined_opts.append({'letter': letter, 'text': e_text, 'text_vi': v_text})
            
        questions.append({
            'number': q_num,
            'question': en_q_text,
            'question_vi': vi_q_text,
            'options': combined_opts,
            'correct': correct_letter,
            'en_transcript': [' '.join(en_transcript_lines)],
            'vi_transcript': [' '.join(vi_transcript_lines)]
        })
    return questions

p1_res = parse_part1(p1_lines)
print(f'Part 1 parsed: {len(p1_res)} questions')
for q in p1_res:
    print(f'Q{q["number"]}: {q["question"][:40]} | Correct: {q["correct"]} | En opts: {len(q["options"])}')
