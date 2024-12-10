import json
import re

with open('./prompt.json') as file:
    data = json.load(file)

sentences1_list = []
sentences2_list = []

for key,value in data.items():
    sentences = value.split(r'.')
    sentences1_list.append(sentences[0])
    sentences2_list.append(sentences[1])
        
out = ''

for x in sentences2_list:
    if 'than' in x:
        out += (x + '.')

print(out)

out_Data = {"TEXT": out}
out_Data_loc = 'out_prompt.json'

with open(out_Data_loc,'w') as f:
    json.dump(out_Data,f)
