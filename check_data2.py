with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('p1_practice_02')
print(content[start:start+1000])
