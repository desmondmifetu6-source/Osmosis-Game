import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances of `\,^\circ\text{C}` with `^\circ\text{C}`
# In raw string / JSON escaped representation:
# `\\,^\\circ\\text{C}` -> `^\\circ\\text{C}`
# `\\,^\\circ\\text{F}` -> `^\\circ\\text{F}`

new_content = content.replace(r'\,^\circ\text{C}', r'^\circ\text{C}')
new_content = new_content.replace(r'\,^\circ\text{F}', r'^\circ\text{F}')

with open('dictionary.json', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully replaced all 75 instances in dictionary.json!")
