import sys
import json
from datetime import datetime
from datetime import timedelta


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


#   __________________________
#
#   CODE EXECUTION STARTS HERE:
#   __________________________


if len(sys.argv) != 2:
    exit()

fileName = sys.argv[1]

with open(fileName, encoding='cp850') as f:
    board = json.load(f)

board = filterTrelloBoard(board)

with open('cleaned_' + board.get('name').split(' ')[0] + '_board.json', 'w', encoding='cp850') as f:
    json.dump(board, f, default=str)

# parse *actions* for card movement
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
            # and add it to the list
            motion.append(value)
motion.reverse()

head = {}
head[board.get('name')] = motion
# output duration to json
with open(board.get('name').split(' ')[0]+'_head.json', 'w') as fp:
    json.dump(head, fp, default=str)
