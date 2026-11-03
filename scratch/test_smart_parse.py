import re

with open('scratch/mock_test_docx_text.txt', encoding='utf-8') as f:
    text = f.read().replace('\xa0', ' ')

lines = [l.strip() for l in text.split('\n') if l.strip()]

# Let's inspect where TRANSCRIPT appears and what comes after
for idx, l in enumerate(lines):
    if l.strip() == 'TRANSCRIPT':
        print(f'Line {idx}: TRANSCRIPT | Next: {lines[idx+1][:60]}')
