import re, json

with open('scratch/mock_test_docx_text.txt', encoding='utf-8') as f:
    full_text = f.read()

# Normalize non-breaking spaces
full_text = full_text.replace('\xa0', ' ')

answers = {
    1: 'D', 2: 'C', 3: 'B', 4: 'C', 5: 'D', 6: 'A', 7: 'B', 8: 'B',
    9: 'B', 10: 'C', 11: 'D', 12: 'A',
    13: 'C', 14: 'C', 15: 'B', 16: 'A',
    17: 'C', 18: 'B', 19: 'D', 20: 'A',
    21: 'C', 22: 'B', 23: 'A', 24: 'C', 25: 'C',
    26: 'C', 27: 'A', 28: 'B', 29: 'A', 30: 'A',
    31: 'A', 32: 'B', 33: 'C', 34: 'D', 35: 'B'
}

raw_lines = [l.strip() for l in full_text.split('\n') if l.strip()]

# Parse Part 1 (lines 1 to 109)
p1_lines = raw_lines[1:110]
part1_questions = []

for q_num in range(1, 9):
    en_idx = None
    vi_idx = None
    for idx, l in enumerate(p1_lines):
        if re.match(rf'^{q_num}\.\s+', l):
            if en_idx is None:
                en_idx = idx
            else:
                vi_idx = idx
                break
    
    next_en_idx = len(p1_lines)
    if q_num < 8:
        for idx, l in enumerate(p1_lines):
            if re.match(rf'^{q_num+1}\.\s+', l):
                next_en_idx = idx
                break
                
    en_block = p1_lines[en_idx:vi_idx]
    vi_block = p1_lines[vi_idx:next_en_idx]
    
    en_q_text = re.sub(rf'^{q_num}\.\s+', '', en_block[0]).strip()
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
    correct_letter = answers[q_num]
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
            
    combined_opts = []
    for i in range(4):
        letter = chr(65 + i)
        e_text = en_opts[i]['text'] if i < len(en_opts) else ''
        v_text = vi_opts[i]['text_vi'] if i < len(vi_opts) else ''
        combined_opts.append({'letter': letter, 'text': e_text, 'text_vi': v_text})
        
    part1_questions.append({
        'number': q_num,
        'question': en_q_text,
        'question_vi': vi_q_text,
        'options': combined_opts,
        'correct': correct_letter,
        'en_transcript': [' '.join(en_transcript_lines)],
        'vi_transcript': [' '.join(vi_transcript_lines)]
    })

print(f'Part 1: {len(part1_questions)} questions parsed')

# Parse Sections for Part 2 and 3
# Let's locate each section by its header
sec_headers = [
    (2, 9, 12, 'QUESTIONS 9 TO 12'),
    (2, 13, 16, 'QUESTIONS 13 TO 16'),
    (2, 17, 20, 'QUESTIONS 17 TO 20'),
    (3, 21, 25, 'QUESTIONS 21 TO 25'),
    (3, 26, 30, 'QUESTIONS 26 TO 30'),
    (3, 31, 35, 'QUESTIONS 31 TO 35')
]

def parse_section(q_start, q_end, block_text):
    # Within block_text:
    # 1. EN questions and options
    # 2. Separator ______
    # 3. VI questions and options
    # 4. TRANSCRIPT
    # 5. EN transcript
    # 6. Separator ______
    # 7. VI transcript
    
    # Split by separator
    parts = re.split(r'_{5,}', block_text)
    # parts[0]: EN questions & options
    # parts[1]: VI questions & options + TRANSCRIPT + EN transcript
    # parts[2]: VI transcript
    
    en_q_block = parts[0].strip()
    middle_block = parts[1].strip()
    vi_transcript = parts[2].strip() if len(parts) > 2 else ""
    
    # Split middle_block at TRANSCRIPT
    mid_parts = re.split(r'\bTRANSCRIPT\b', middle_block, flags=re.I)
    vi_q_block = mid_parts[0].strip()
    en_transcript = mid_parts[1].strip() if len(mid_parts) > 1 else ""
    
    # Parse EN questions & options
    en_qs = {}
    for q_n in range(q_start, q_end + 1):
        # find pattern: q_n. <text> up to next q or end
        next_n = q_n + 1 if q_n < q_end else 9999
        pattern = rf'(?:^|\n){q_n}\.\s+(.*?)(?=(?:^|\n){next_n}\.\s+|$)'
        m = re.search(pattern, en_q_block, re.S)
        if m:
            chunk = m.group(1).strip()
            # Extract question line (up to first option A.)
            opt_m = re.search(r'([A-D]\..*)$', chunk, re.S)
            if opt_m:
                q_text = chunk[:opt_m.start()].strip()
                opts_str = opt_m.group(1).strip()
            else:
                q_text = chunk
                opts_str = ""
            opts = re.findall(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))', opts_str, re.S)
            en_qs[q_n] = {
                'text': q_text,
                'options': {letter: o_text.strip() for letter, o_text in opts}
            }
            
    # Parse VI questions & options
    vi_qs = {}
    for q_n in range(q_start, q_end + 1):
        next_n = q_n + 1 if q_n < q_end else 9999
        pattern = rf'(?:^|\n){q_n}\.\s+(.*?)(?=(?:^|\n){next_n}\.\s+|$)'
        m = re.search(pattern, vi_q_block, re.S)
        if m:
            chunk = m.group(1).strip()
            opt_m = re.search(r'([A-D]\..*)$', chunk, re.S)
            if opt_m:
                q_text = chunk[:opt_m.start()].strip()
                opts_str = opt_m.group(1).strip()
            else:
                q_text = chunk
                opts_str = ""
            opts = re.findall(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))', opts_str, re.S)
            vi_qs[q_n] = {
                'text': q_text,
                'options': {letter: o_text.strip() for letter, o_text in opts}
            }
            
    # Assemble section questions
    sec_questions = []
    for q_n in range(q_start, q_end + 1):
        eq = en_qs.get(q_n, {'text': '', 'options': {}})
        vq = vi_qs.get(q_n, {'text': '', 'options': {}})
        
        opts = []
        for i in range(4):
            letter = chr(65 + i)
            opts.append({
                'letter': letter,
                'text': eq['options'].get(letter, ''),
                'text_vi': vq['options'].get(letter, '')
            })
            
        sec_questions.append({
            'number': q_n,
            'question': eq['text'],
            'question_vi': vq['text'],
            'options': opts,
            'correct': answers[q_n]
        })
        
    return {
        'questions': sec_questions,
        'en_transcript': [line.strip() for line in en_transcript.split('\n') if line.strip()],
        'vi_transcript': [line.strip() for line in vi_transcript.split('\n') if line.strip()]
    }

# Slice full_text by section headers
sections_data = []
for i in range(len(sec_headers)):
    part_num, q_s, q_e, title = sec_headers[i]
    start_pos = full_text.find(title)
    if i < len(sec_headers) - 1:
        next_title = sec_headers[i+1][3]
        end_pos = full_text.find(next_title)
        block = full_text[start_pos + len(title):end_pos]
    else:
        block = full_text[start_pos + len(title):]
        
    sec_res = parse_section(q_s, q_e, block)
    sec_res['part'] = part_num
    sec_res['q_start'] = q_s
    sec_res['q_end'] = q_e
    sec_res['title'] = title
    sections_data.append(sec_res)

print(f'Parsed {len(sections_data)} sections for Part 2 & 3')
for s in sections_data:
    print(f'{s["title"]}: {len(s["questions"])} questions, {len(s["en_transcript"])} en lines, {len(s["vi_transcript"])} vi lines')
