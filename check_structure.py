import json

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Just print the first Practice of Part 2 to understand the structure
start = content.find('"id": "p2_practice_01"')
end = content.find('"id": "p2_practice_02"')
print(content[start:start+1000])
