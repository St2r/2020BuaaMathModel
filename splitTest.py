import json
import editDistance

end = {'TAG', 'TAA', 'TGA'}


def judge(seq1: str, seq2: str) -> bool:
    count = 0
    for i in range(10):
        if seq1[i] != seq2[i]:
            count += 1
    return count < 4


if __name__ == '__main__':
    content = ''
    with open('mini/LC534418.txt', 'r') as f:
        for line in f.readlines():
            content += line.strip().replace('\n', '')
    with open('data/refTargetSeq.json') as f:
        for target in json.load(f)['gene']:
            t = content[target['start'] - 10: target['end'] + 10]
            t_start = t.find('ATG')
            while not judge(target['seq'], t[t_start: t_start + 10]):
                t_start = t.find('ATG', t_start + 1)
            t_end = t_start + 3
            while not end.__contains__(t[t_end - 3: t_end]):
                t_end += 3
                # print(t[t_end - 3: t_end])
                # input(t[t_start: t_end])

            print('split:\t' + t[t_start: t_end])
            print('origin:\t' + target['seq'])
            print()
