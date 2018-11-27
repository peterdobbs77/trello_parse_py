import sys
import json
from datetime import datetime
from datetime import timedelta

if len(sys.argv) != 1:
    exit()

fileName = sys.argv[0]

with open(fileName) as f:
    card = json.load(f)

motion = []
for a in card.get('actions'):
    if a.get('type') == "updateCard":
        if 'listBefore' in a.get('data'):
            value = {
                'card': a.get('data').get('card'),
                'before': a.get('data').get('listBefore'),
                'after': a.get('data').get('listAfter'),
                'timestamp': a.get('date')
            }
            motion.append(value)
motion.reverse()

with open(card.get('name')+'_motion.json', 'w') as fp:
    json.dump(motion, fp)

# delivery time
start_time = datetime.strptime(motion[0].get(
    'timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')
deliv_time = datetime.strptime(
    motion[(motion.__len__() - 1)].get('timestamp'), '%Y-%m-%dT%H:%M:%S.%fZ')
delivery_time = deliv_time - start_time
print('time for delivery:', delivery_time)

# TODO: need to fix this for if any utilities were redelivered or cards were used for previous delivery season

# check for duplicates (shows if steps were repeated)
seen = set()
for m in motion:
    if m.get('after').get('name') in seen:
        print('duplicates of:', m.get('after').get('name'))
    seen.add(m.get('after').get('name'))
