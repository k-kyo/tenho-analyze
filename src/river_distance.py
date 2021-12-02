import json

PIVOT = [['5m']*7,
         ['5p']*7,
         ['5s']*7,
         ['1m']*7,]

with open('./input/distance.json', 'r', encoding='utf-8') as d:
    distance_data = json.load(d)


def hai_distance(a, b):
    if a == b:
        return 0.
    elif 'z' == a[-1]:
        return distance_data['字牌'][f'{b[0]}-z']
    elif 'z' == b[-1]:
        return distance_data['字牌'][f'{a[0]}-z']
    elif a[-1] == b[-1]:
        return distance_data['同種'][f'{a[0]}-{b[0]}']
    elif ('m' == a[-1] and 'p' == b[-1]) or ('p' == a[-1] and 'm' == b[-1]):
        return distance_data['異種'][f'{a}-{b}'] if 'm' == a[-1] else distance_data['異種'][f'{b}-{a}']
    elif ('p' == a[-1] and 's' == b[-1]) or ('s' == a[-1] and 'p' == b[-1]):
        return distance_data['異種'][f'{a}-{b}'] if 'p' == a[-1] else distance_data['異種'][f'{b}-{a}']
    elif ('s' == a[-1] and 'm' == b[-1]) or ('m' == a[-1] and 's' == b[-1]):
        return distance_data['異種'][f'{a}-{b}'] if 's' == a[-1] else distance_data['異種'][f'{b}-{a}']
    else:
        raise ValueError("error!")


def sutehai_distance(a_list, b_list):
    return sum([hai_distance(a, b) for a, b in zip(a_list, b_list)])


def pivot_distance(target):
    return [sutehai_distance(target, p) for p in PIVOT]
