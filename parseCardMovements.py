import sys
import json
from datetime import datetime
from datetime import timedelta


def timestamp_to_datetime(ts):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')


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
                'card': a.get('data').get('card'),
                'before': a.get('data').get('listBefore'),
                'after': a.get('data').get('listAfter'),
                'timestamp': a.get('date')
            }
            # and add it to the list
            motion.append(value)
motion.reverse()
# output motion to json
with open('.\\_motion\\'+card.get('name')+'_motion.json', 'w') as fp:
    json.dump(motion, fp)

# calculate process time
# TODO: need to fix this calculation to distinguish redelivered utilities
#   from cards were used in previous delivery season
start_time = timestamp_to_datetime(motion[0].get('timestamp'))
final_time = timestamp_to_datetime(
    motion[(motion.__len__() - 1)].get('timestamp'))
process_time = final_time - start_time
print('time for delivery:', process_time)


# check for duplicates (shows if steps were repeated)
seen = set()
for m in motion:
    if m.get('after').get('name') in seen:
        print('duplicates of:', m.get('after').get('name'))
    seen.add(m.get('after').get('name'))

# calculate time spent in each list (including if the step was repeated)
previous = start_time
duration = {}
for m in motion:
    ts = timestamp_to_datetime(m.get('timestamp'))
    dur = ts - previous
    if m.get('before').get('name') in duration:
        duration[m.get('before').get('name')+'_2'] = dur
    else:
        duration[m.get('before').get('name')] = dur
    previous = ts

# output duration to json
with open('.\\_duration\\'+card.get('name')+'_duration.json', 'w') as fp:
    json.dump(duration, fp, default=str)
