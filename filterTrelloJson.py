import sys
import json

if len(sys.argv) != 2:
    exit()

fileName = sys.argv[1]

with open(fileName) as f:
    card = json.load(f)

filtered_card = {}
filtered_card['name'] = card.get('name')
filtered_card['actions'] = card.get('actions')

with open(fileName, 'w') as fp:
    json.dump(filtered_card, fp)
