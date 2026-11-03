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
        'part': 1,
        'question': en_q_text,
        'question_vi': vi_q_text,
        'options': combined_opts,
        'correct': correct_letter,
        'en_transcript': [' '.join(en_transcript_lines)],
        'vi_transcript': [' '.join(vi_transcript_lines)]
    })

# 2. PARSE PART 2 & PART 3 SECTIONS
sections_bounds = [
    (2, 9, 12, "Conversation 01", 111, 181),
    (2, 13, 16, "Conversation 02", 181, 247),
    (2, 17, 20, "Conversation 03", 247, 390),
    (3, 21, 25, "Talk 01", 391, 443),
    (3, 26, 30, "Talk 02", 443, 482),
    (3, 31, 35, "Talk 03", 482, len(lines))
]

def format_highlights(trans_lines, is_vi=False):
    # If is_vi is False, find [9], [10], etc. and highlight
    formatted = []
    for line in trans_lines:
        if not is_vi:
            # Highlight [X] ...
            # replace [X] with <span class="highlight">[X]
            # If line has [X], highlight from [X] to end of sentence or clause
            hl_line = re.sub(r'(\[\d+\].*?)(?=(?:\[\d+\]|$))', lambda m: f'<span class="highlight">{m.group(1).strip()}</span> ', line)
            formatted.append(hl_line.strip())
        else:
            hl_line = re.sub(r'(\(\d+\).*?)(?=(?:\(\d+\)|$))', lambda m: f'<span class="highlight">{m.group(1).strip()}</span> ', line)
            formatted.append(hl_line.strip())
    return formatted

def parse_multi_q_section(part_num, q_start, q_end, sec_title, start_idx, end_idx):
    sec_lines = lines[start_idx:end_idx]
    
    trans_idx = None
    for idx, l in enumerate(sec_lines):
        if l == 'TRANSCRIPT':
            trans_idx = idx
            break
            
    q_lines = sec_lines[1:trans_idx]
    vi_q_start_idx = None
    for idx, l in enumerate(q_lines):
        if re.match(rf'^{q_start}\.\s+', l) and any(c in 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ' for c in l.lower()):
            vi_q_start_idx = idx
            break
            
    en_q_lines = q_lines[:vi_q_start_idx]
    vi_q_lines = q_lines[vi_q_start_idx:]
    
    def extract_qs(q_list, is_vi=False):
        full_chunk = '\n'.join(q_list)
        res = {}
        for q_n in range(q_start, q_end + 1):
            next_n = q_n + 1 if q_n < q_end else 9999
            pattern = rf'(?:^|\n){q_n}\.\s+(.*?)(?=(?:^|\n){next_n}\.\s+|$)'
            m = re.search(pattern, full_chunk, re.S)
            if m:
                raw_chunk = m.group(1).strip()
                opt_m = re.search(r'([A-D]\..*)$', raw_chunk, re.S)
                if opt_m:
                    q_text = raw_chunk[:opt_m.start()].strip()
                    opts_str = opt_m.group(1).strip()
                else:
                    q_text = raw_chunk
                    opts_str = ""
                opts = re.findall(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))', opts_str, re.S)
                opts_dict = {l: t.strip() for l, t in opts}
                res[q_n] = {'text': q_text, 'options': opts_dict}
            else:
                res[q_n] = {'text': '', 'options': {}}
        return res
        
    en_parsed = extract_qs(en_q_lines, is_vi=False)
    vi_parsed = extract_qs(vi_q_lines, is_vi=True)
    
    post_trans = sec_lines[trans_idx+1:]
    en_trans_lines = []
    vi_trans_lines = []
    in_vi = False
    for l in post_trans:
        if re.match(r'^_{5,}$', l):
            in_vi = True
            continue
        if not in_vi and (l.startswith('Lễ tân:') or l.startswith('Khách:') or l.startswith('Nam sinh:') or l.startswith('Tên tôi là') or l.startswith('Chào buổi chiều') or l.startswith('(31)')):
            in_vi = True
            
        if in_vi:
            vi_trans_lines.append(l)
        else:
            en_trans_lines.append(l)
            
    formatted_en = format_highlights(en_trans_lines, is_vi=False)
    formatted_vi = format_highlights(vi_trans_lines, is_vi=True)
    
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
            'part': part_num,
            'section_title': sec_title,
            'question': eq['text'],
            'question_vi': vq['text'],
            'options': opts,
            'correct': answers[q_n],
            'en_transcript': formatted_en,
            'vi_transcript': formatted_vi
        })
        
    return {
        'part': part_num,
        'title': sec_title,
        'q_start': q_start,
        'q_end': q_end,
        'questions': sec_questions,
        'en_transcript': formatted_en,
        'vi_transcript': formatted_vi
    }

parsed_sections = []
for b in sections_bounds:
    sec = parse_multi_q_section(*b)
    parsed_sections.append(sec)

# Assemble all 35 questions
all_questions = []
# Part 1 questions
for q in part1_questions:
    all_questions.append(q)

for s in parsed_sections:
    for q in s['questions']:
        all_questions.append(q)

print(f'Total questions assembled: {len(all_questions)}')

mock_test_object = {
    'id': 'vstep_mock_test_01',
    'title': 'VSTEP LISTENING MOCK TEST 01',
    'subtitle': 'Đề thi thử toàn diện chuẩn định dạng kỳ thi VSTEP bậc 3-5 (B1-B2-C1)',
    'duration': 2400, # 40 minutes in seconds
    'audio': 'LISTENING MOCK TEST/AUDIO/MOCK TEST.mp3',
    'totalQuestions': 35,
    'parts': [
        {
            'part': 1,
            'title': 'PART 01: SHORT TALKS / CONVERSATIONS',
            'description': 'Gồm 8 câu hỏi ngắn. Chọn đáp án đúng A, B, C hoặc D.',
            'q_range': [1, 8]
        },
        {
            'part': 2,
            'title': 'PART 02: LONG CONVERSATIONS',
            'description': 'Gồm 3 bài hội thoại dài (Câu 09 - 20). Mỗi bài gồm 4 câu hỏi.',
            'q_range': [9, 20],
            'sections': [
                {'title': 'Conversation 01 (Câu 09 - 12)', 'q_range': [9, 12]},
                {'title': 'Conversation 02 (Câu 13 - 16)', 'q_range': [13, 16]},
                {'title': 'Conversation 03 (Câu 17 - 20)', 'q_range': [17, 20]}
            ]
        },
        {
            'part': 3,
            'title': 'PART 03: LONG TALKS / LECTURES',
            'description': 'Gồm 3 bài nói/bài giảng học thuật (Câu 21 - 35). Mỗi bài gồm 5 câu hỏi.',
            'q_range': [21, 35],
            'sections': [
                {'title': 'Talk 01 (Câu 21 - 25)', 'q_range': [21, 25]},
                {'title': 'Talk 02 (Câu 26 - 30)', 'q_range': [26, 30]},
                {'title': 'Talk 03 (Câu 31 - 35)', 'q_range': [31, 35]}
            ]
        }
    ],
    'sections': parsed_sections,
    'questions': all_questions
}

output_js = f"window.VSTEP_MOCK_TEST_DATA = {json.dumps(mock_test_object, ensure_ascii=False, indent=2)};\n"

with open('mock_test_data.js', 'w', encoding='utf-8') as f:
    f.write(output_js)

print("Successfully written mock_test_data.js!")
