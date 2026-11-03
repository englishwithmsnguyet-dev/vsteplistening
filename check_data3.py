with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('p1_practice_01')
end = content.find('p1_practice_02')
print("Practice 01 transcript count:", content[start:end].count('"transcript":'))

start2 = content.find('p1_practice_02')
end2 = content.find('p1_practice_03')
print("Practice 02 transcript count:", content[start2:end2].count('"transcript":'))

start3 = content.find('p1_practice_03')
end3 = content.find('p1_practice_04')
print("Practice 03 transcript count:", content[start3:end3].count('"transcript":'))
