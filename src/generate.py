from json import dump
from glob import glob
from joblib import Parallel, delayed
from mjscore_split import kyoku_split
from river_distance import pivot_distance
from syanten import syanten_yukou


NUMBER = 7
SUIT_ORDER = ['m', 'p', 's', 'z']


def kyoku_analyze(tehai_dic, stream):
    sutehai_dic = {'1': [], '2': [], '3': [], '4': []}
    for oc in stream:
        if len(oc) == 2:
            continue
        hm = oc[0]
        action = oc[1]
        num = int(oc[2])-1
        suit = SUIT_ORDER.index(oc[3].lower())
        s = oc[2:4].lower()
        if action == 'G':
            tehai_dic[hm][0][suit][num] += 1
        elif action == 'd' or action == 'D':
            if len(sutehai_dic[hm]) < NUMBER:
                tehai_dic[hm][0][suit][num] -= 1
                sutehai_dic[hm].append(s)
            if len(sutehai_dic[hm]) == NUMBER:
                distance = pivot_distance(sutehai_dic[hm])
                label = syanten_yukou(tehai_dic[hm])
                yield {'distance': distance, 'label': label}
                if sum([len(sutehai_dic[str(i)]) == NUMBER for i in range(1, 5)]) == 4:
                    return
        elif action == 'N':
            tehai_dic[hm][0][suit][num] -= 2
            tehai_dic[hm][1].append([0, s, prev_s, prev_hm])
        elif action == 'C':
            tehai_dic[hm][0][suit][num] -= 1
            tehai_dic[hm][0][suit][int(oc[-2])-1] -= 1
            tehai_dic[hm][1].append([1, s if min(prev_num, num) == num else prev_s, prev_s, prev_hm])
        elif action == 'K':
            if prev_action == 'd' or prev_action == 'D':
                tehai_dic[hm][0][suit][num] -= 3
                tehai_dic[hm][1].append([3, s, prev_s, prev_hm])
            elif tehai_dic[hm][0][suit][num] == 4:
                tehai_dic[hm][0][suit][num] -= 4
                tehai_dic[hm][1].append([2, s, s, prev_hm])
            else:
                tehai_dic[hm][0][suit][num] -= 1
                for f in tehai_dic[hm][1]:
                    if f[2] == s:
                        f[0] = 4
                        break
        prev_hm = hm
        prev_action = action
        prev_num = num
        prev_s = s


def process(tehai_dic, stream):
    results = []
    for result in kyoku_analyze(tehai_dic, stream):
        results.append(result)
    return results


def generate(filepaths):
    l = len(filepaths)
    for i, filepath in enumerate(filepaths):
        print(i+1, '/', l)
        results = Parallel(n_jobs = -1)(delayed(process)(tehai_dic, stream)for tehai_dic, stream in kyoku_split(filepath))
        for result in results:
            yield result


def main():
    filepaths = glob('./mjscore/2013/03/11/*.txt')
    # filepaths = glob('./mjscore/2013/03/11/2013031100gm-00a9-0000-0a2171cd&tw=0.txt')
    results = []
    for result in generate(filepaths):
        results.append(result)
    with open('./result.json', mode='w') as f:
        dump(results, f)


if __name__ == '__main__':
    main()
