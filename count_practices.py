import re
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    
p2_matches = re.findall(r'"id": "(p2_practice_\d+)"', content)
p3_matches = re.findall(r'"id": "(p3_practice_\d+)"', content)

print("Part 2 practices:", len(p2_matches), p2_matches)
print("Part 3 practices:", len(p3_matches), p3_matches)
