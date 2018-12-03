import sys
import json
from datetime import datetime
from datetime import timedelta

#   __________________________
#
#   CODE EXECUTION STARTS HERE:
#   __________________________

if len(sys.argv) != 2:
    exit()

fileName = sys.argv[1]

with open(fileName) as f:
    card = json.load(f)

# parse *actions* for card movement
motion = []
for a in card.get('actions'):
    if a.get('type') == "updateCard":
        if 'listBefore' in a.get('data'):
            # build new json string entry
            value = {
                'before': a.get('data').get('listBefore').get('name'),
                'after': a.get('data').get('listAfter').get('name'),
                'timestamp': datetime.strptime(a.get('date'), '%Y-%m-%dT%H:%M:%S.%fZ')
            }
            # and add it to the list
            motion.append(value)
motion.reverse()

# calculate process time
# TODO: need to fix this calculation to distinguish a rerun processes
#   from cards used in previous process term
start_time = motion[0].get('timestamp')
final_time = motion[(motion.__len__() - 1)].get('timestamp')
process_time = final_time - start_time
print('time for process:', process_time)


# check for duplicates (shows if steps were repeated)
seen = set()
for m in motion:
    if m.get('after') in seen:
        print('duplicates of:', m.get('after'))
    seen.add(m.get('after'))

# calculate time spent in each list (including if the step was repeated)
previous = start_time
for m in motion:
    ts = m.get('timestamp')
    dur = ts - previous
    m['durationBefore'] = dur.seconds
    previous = ts

head = {}
head[card.get('name')] = motion
# output duration to json
with open(card.get('name')+'_head.json', 'w') as fp:
    json.dump(head, fp, default=str)
