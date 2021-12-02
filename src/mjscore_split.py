import re
from glob import glob

SUIT_ORDER = ['m', 'p', 's', 'z']

def file_readline(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def file_split(file_path):
    lis = file_readline(file_path).replace(' ', '').split('\n')
    for i, row in enumerate(lis):
        if re.match('[東南西北]\d局', row):
            start = i
        elif not row:
            end = i
            yield lis[start:end+1]
        elif row == '----試合結果----':
            break


def hai_replace(s):
    return s.replace('東', '1z')\
            .replace('南', '2z')\
            .replace('西', '3z')\
            .replace('北', '4z')\
            .replace('白', '5z')\
            .replace('発', '6z')\
            .replace('中', '7z')\


def kyoku_split(file_path):
    for block in file_split(file_path):
        haipai_dic = split_haipai(block)
        action_list = split_action(block)
        yield (haipai_dic, action_list)


def replace_haipai_split(s):
    s = hai_replace(s)
    return [a+b for a, b in zip(s[::2], s[1::2])]


def replace_sutehai_split(s):
    result = []
    s = hai_replace(s)
    while s:
        if s[1] == 'C' or s[1] == 'N':
            result.append(s[:6])
            s = s[6:]
        elif s[1] == 'R' or s[1] == 'A':
            result.append(s[:2])
            s = s[2:]
        else:
            result.append(s[:4])
            s = s[4:]
    return result


def split_haipai(block):
    haipai_dic = {}
    for row in block[2:6]:
        i = row[1]
        haipai = replace_haipai_split(row[4:])
        haipai_dic[i] = tehai_change(haipai)
    return haipai_dic


def split_action(block):
    action_list = []
    for row in block[7:-1]:
        row = row[1:]
        row_action = replace_sutehai_split(row)
        action_list.extend(row_action)
    return action_list


def tehai_change(hai_list):
    tehai = [[[0]*9, [0]*9, [0]*9, [0]*7], []]
    for hai in hai_list:
        num = int(hai[0])-1
        suit = SUIT_ORDER.index(hai[1].lower())
        tehai[0][suit][num] += 1
    return tehai
