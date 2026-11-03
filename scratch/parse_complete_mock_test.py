import re, json

with open('scratch/mock_test_docx_text.txt', encoding='utf-8') as f:
    text = f.read().replace('\xa0', ' ')

lines = [l.strip() for l in text.split('\n') if l.strip()]

answers = {
    1: 'D', 2: 'C', 3: 'B', 4: 'C', 5: 'D', 6: 'A', 7: 'B', 8: 'B',
    9: 'B', 10: 'C', 11: 'D', 12: 'A',
    13: 'C', 14: 'C', 15: 'B', 16: 'A',
    17: 'C', 18: 'B', 19: 'D', 20: 'A',
    21: 'C', 22: 'B', 23: 'A', 24: 'C', 25: 'C',
    26: 'C', 27: 'A', 28: 'B', 29: 'A', 30: 'A',
    31: 'A', 32: 'B', 33: 'C', 34: 'D', 35: 'B'
}

# 1. PARSE PART 1 (Questions 1 - 8)
p1_lines = lines[1:110]
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

# 2. PARSE PART 2 & PART 3 SECTIONS
# Section 1: Q9-12 (lines 111 to 180)
# Section 2: Q13-16 (lines 181 to 246)
# Section 3: Q17-20 (lines 247 to 389)
# Section 4: Q21-25 (lines 391 to 442)
# Section 5: Q26-30 (lines 443 to 481)
# Section 6: Q31-35 (lines 482 to end)

sections_bounds = [
    (2, 9, 12, "Part 2 - Conversation 01", 111, 181),
    (2, 13, 16, "Part 2 - Conversation 02", 181, 247),
    (2, 17, 20, "Part 2 - Conversation 03", 247, 390),
    (3, 21, 25, "Part 3 - Talk 01", 391, 443),
    (3, 26, 30, "Part 3 - Talk 02", 443, 482),
    (3, 31, 35, "Part 3 - Talk 03", 482, len(lines))
]

def parse_multi_q_section(part_num, q_start, q_end, sec_title, start_idx, end_idx):
    sec_lines = lines[start_idx:end_idx]
    
    # 1. Locate TRANSCRIPT index
    trans_idx = None
    for idx, l in enumerate(sec_lines):
        if l == 'TRANSCRIPT':
            trans_idx = idx
            break
            
    # Lines before TRANSCRIPT are questions (EN then VI)
    q_lines = sec_lines[1:trans_idx]
    # Find where Vietnamese questions begin (look for q_start. in Vietnamese)
    vi_q_start_idx = None
    for idx, l in enumerate(q_lines):
        if re.match(rf'^{q_start}\.\s+', l) and any(c in 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ' for c in l.lower()):
            vi_q_start_idx = idx
            break
            
    en_q_lines = q_lines[:vi_q_start_idx]
    vi_q_lines = q_lines[vi_q_start_idx:]
    
    # Helper to parse Q & options from a list of lines
    def extract_qs(q_list, is_vi=False):
        full_chunk = '\n'.join(q_list)
        res = {}
        for q_n in range(q_start, q_end + 1):
            next_n = q_n + 1 if q_n < q_end else 9999
            pattern = rf'(?:^|\n){q_n}\.\s+(.*?)(?=(?:^|\n){next_n}\.\s+|$)'
            m = re.search(pattern, full_chunk, re.S)
            if m:
                raw_chunk = m.group(1).strip()
                # Find options
                opt_m = re.search(r'([A-D]\..*)$', raw_chunk, re.S)
                if opt_m:
                    q_text = raw_chunk[:opt_m.start()].strip()
                    opts_str = opt_m.group(1).strip()
                else:
                    q_text = raw_chunk
                    opts_str = ""
                # Parse A. B. C. D.
                opts = re.findall(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))', opts_str, re.S)
                opts_dict = {l: t.strip() for l, t in opts}
                res[q_n] = {'text': q_text, 'options': opts_dict}
            else:
                res[q_n] = {'text': '', 'options': {}}
        return res
        
    en_parsed = extract_qs(en_q_lines, is_vi=False)
    vi_parsed = extract_qs(vi_q_lines, is_vi=True)
    
    # 2. Parse transcripts (after trans_idx)
    post_trans = sec_lines[trans_idx+1:]
    # Find separator or transition to Vietnamese
    # We can identify VI transcript by looking for Vietnamese speaker prefix or high diacritic count
    en_trans_lines = []
    vi_trans_lines = []
    in_vi = False
    for l in post_trans:
        if re.match(r'^_{5,}$', l):
            in_vi = True
            continue
        # Also detect Vietnamese speaker prefix like "Lễ tân:", "Khách:", "Nam sinh:", "Tên tôi là"
        if not in_vi and (l.startswith('Lễ tân:') or l.startswith('Khách:') or l.startswith('Nam sinh:') or l.startswith('Tên tôi là') or l.startswith('Chào buổi chiều') or l.startswith('(31)')):
            in_vi = True
            
        if in_vi:
            vi_trans_lines.append(l)
        else:
            en_trans_lines.append(l)
            
    # Combine questions
    sec_questions = []
    for q_n in range(q_start, q_end + 1):
        eq = en_parsed.get(q_n, {'text': '', 'options': {}})
        vq = vi_parsed.get(q_n, {'text': '', 'options': {}})
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
        'part': part_num,
        'q_start': q_start,
        'q_end': q_end,
        'title': sec_title,
        'questions': sec_questions,
        'en_transcript': en_trans_lines,
        'vi_transcript': vi_trans_lines
    }

parsed_sections = []
for b in sections_bounds:
    sec = parse_multi_q_section(*b)
    parsed_sections.append(sec)

print(f'Parsed {len(parsed_sections)} multi-question sections')
total_q = len(part1_questions) + sum(len(s['questions']) for s in parsed_sections)
print(f'Total questions parsed: {total_q} / 35')

for s in parsed_sections:
    print(f"{s['title']}: {len(s['questions'])} qs, EN trans: {len(s['en_transcript'])} lines, VI trans: {len(s['vi_transcript'])} lines")
