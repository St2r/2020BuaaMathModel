# 此文件用于统计突变
import os
import json
import pandas as pd


def statistic(target: tuple) -> dict:
    ans = dict()
    for file in target:
        with open(file, 'r') as f:
            content = json.load(f)
            for gene in content:
                for mutation in content[gene]:
                    if mutation['type'] == 'replace':
                        key = '%d_%s_%s' % (mutation['position'], mutation['source'], mutation['target'])
                        if mutation['target'] not in {'A', 'T', 'C', 'G'}:
                            continue
                        if key not in ans:
                            ans[key] = 0
                        ans[key] += 1
    return ans


def toCsv(pos_bias: int, seq: str, source: dict, output: str = None):
    def get_source_pair(position: int, seq: str):
        c_start = (position - 1) // 3 * 3
        return seq[c_start: c_start + 3]

    def get_target_pair(source_pair: str, position: int, target: str):
        c_pos = (position - 1) % 3
        return source_pair[:c_pos] + target + source_pair[c_pos + 1:]

    l_position = list()
    l_source = list()
    l_target = list()
    l_source_pair = list()
    l_target_pair = list()
    l_count = list()

    for s in source:
        sub = s.split('_')
        l_position.append(int(sub[0]) + pos_bias)
        l_source.append(sub[1])
        l_target.append(sub[2])
        source_pair = get_source_pair(int(sub[0]), seq)
        target_pair = get_target_pair(source_pair, int(sub[0]), sub[2])
        l_source_pair.append(source_pair)
        l_target_pair.append(target_pair)
        l_count.append(source[s])
    d = pd.DataFrame({
        'position': l_position,
        'source': l_source,
        'target': l_target,
        'source_pair': l_source_pair,
        'target_pair': l_target_pair,
        'count': l_count
    })

    if output != None:
        d.to_csv(output, index=False, sep=',')
    return d


if __name__ == '__main__':
    targetGene = '7a'

    targetFiles = (
        os.path.join('data', '2020-March-Gene', '_mutation_%s.json' % targetGene),
        os.path.join('data', '2020-April-Gene', '_mutation_%s.json' % targetGene),
        os.path.join('data', '2020-May-Gene', '_mutation_%s.json' % targetGene),
        os.path.join('data', '2020-June-Gene', '_mutation_%s.json' % targetGene),
        os.path.join('data', '2020-July(14)-Gene', '_mutation_%s.json' % targetGene),
    )

    s = statistic(targetFiles)

    with open('data/refTargetSeq.json', 'r') as f:
        for g in json.load(f)['gene']:
            if g['name'] == targetGene:
                start = g['start'] - 1
                seq = g['seq']
                break

    c = toCsv(start, seq, s, output=os.path.join('data', 'mutation', 'mutation_%s.csv' % targetGene))
