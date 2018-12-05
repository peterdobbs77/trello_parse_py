# Python 3.6.6

import sys
import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np


def fixTrelloTimestamp(ts):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%x %X')


def filterTrelloBoard(board):
    filtered_board = {}
    filtered_board['name'] = board.get('name')
    actions = []
    for a in board.get('actions'):
        list_item = {}
        list_item['data'] = a.get('data')
        for x in list_item['data']:
            if x in ['text', 'deactivated']:
                continue
            if 'name' in a.get('data')[x]:
                list_item.get('data')[x] = a.get('data').get(x).get('name')
        list_item['actor'] = a.get('memberCreator').get('fullName')
        list_item['type'] = a.get('type')
        list_item['date'] = fixTrelloTimestamp(a.get('date'))
        actions.append(list_item)
    filtered_board['actions'] = actions
    for each in ['cards', 'lists', 'members']:
        gen = []
        for item in board.get(each):
            gen.append(item.get('name'))
        filtered_board[each] = gen
    return filtered_board


def getCardMotionFromBoardActions(board):
    motion = []
    for a in board.get('actions'):
        if a.get('type') == "updateCard":
            if 'listBefore' in a.get('data'):
                # build new json string entry
                value = {
                    'card': a.get('data').get('card'),
                    'before': a.get('data').get('listBefore'),
                    'after': a.get('data').get('listAfter'),
                    'timestamp': a.get('date')
                }
                motion.append(value)
    motion.reverse()
    return motion


# SETUP
if len(sys.argv) != 2:
    exit()

fileName = sys.argv[1]

with open(fileName, encoding='cp850') as f:
    board = json.load(f)

# GET ONLY STUFF THAT MATTERS
board = filterTrelloBoard(board)
# GET ONLY MOTION INFO / DEIDENTIFY ACTIONS
motion = getCardMotionFromBoardActions(board)

# CALCULATE LENGTH OF WHOLE BOARD PROCESS
start_time = datetime.strptime(motion[0].get('timestamp'), '%x %X')
final_time = datetime.strptime(
    motion[(motion.__len__() - 1)].get('timestamp'), '%x %X')
process_time = final_time - start_time
print('time for process:', process_time)

# ANALYSIS
df = pd.DataFrame(motion)
# df['timestamp'] = pd.to_datetime(df.timestamp)
# df = df.sort_values('timestamp', ascending=False)
# df = df.sort_values('card', ascending=True)

df.to_csv(board.get('name')+'.csv')

# pd.pivot_table(df, values='after', index='after',
#    aggfunc=[pd.Series.nunique, np.cumsum(pd.Series.nunique)])
