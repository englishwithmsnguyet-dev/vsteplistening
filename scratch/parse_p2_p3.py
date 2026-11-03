import re, json

with open('scratch/mock_test_docx_text.txt', encoding='utf-8') as f:
    text = f.read()

# All verified answers
answers = {
    1: 'D', 2: 'C', 3: 'B', 4: 'C', 5: 'D', 6: 'A', 7: 'B', 8: 'B',
    9: 'B', 10: 'C', 11: 'D', 12: 'A',
    13: 'C', 14: 'C', 15: 'B', 16: 'A',
    17: 'C', 18: 'B', 19: 'D', 20: 'A',
    21: 'C', 22: 'B', 23: 'A', 24: 'C', 25: 'C',
    26: 'C', 27: 'A', 28: 'B', 29: 'A', 30: 'A',
    31: 'A', 32: 'B', 33: 'C', 34: 'D', 35: 'B'
}

# The sections for Part 2 and 3
sections_meta = [
    {'part': 2, 'q_range': (9, 12), 'title': 'QUESTIONS 9 TO 12'},
    {'part': 2, 'q_range': (13, 16), 'title': 'QUESTIONS 13 TO 16'},
    {'part': 2, 'q_range': (17, 20), 'title': 'QUESTIONS 17 TO 20'},
    {'part': 3, 'q_range': (21, 25), 'title': 'QUESTIONS 21 TO 25'},
    {'part': 3, 'q_range': (26, 30), 'title': 'QUESTIONS 26 TO 30'},
    {'part': 3, 'q_range': (31, 35), 'title': 'QUESTIONS 31 TO 35'},
]

# Helper to split options from string like "A. One day. B. Two days. C. Three days. D. Four days."
def parse_options_from_text(opt_text):
    # Regex find A. ... B. ... C. ... D. ...
    pattern = r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))'
    matches = re.findall(pattern, opt_text, re.S)
    res = {}
    for letter, content in matches:
        res[letter] = content.strip()
    return res

print("Section parser helper ready")
