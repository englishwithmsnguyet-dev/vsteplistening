import json

# read data.js and try to parse it
# Actually, let's just find the first question of p1_practice_01
with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('p1_practice_01')
end = content.find('p1_practice_02')
print(content[start:start+1000])
