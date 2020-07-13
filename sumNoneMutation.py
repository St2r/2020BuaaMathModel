import os
import json

targetFolders = (
    '2020-March-Gene',
    '2020-April-Gene',
    '2020-May-Gene',
    '2020-June-Gene',
    '2020-July(14)-Gene'
)
targetGene = 'M'


def getNoneMutationSet() -> set:
    ans = set()
    for targetFolder in targetFolders:
        with open(os.path.join('data', targetFolder, '_mutation_%s.json' % targetGene)) as f:
            m = json.load(f)
            for gene in m:
                if len(m[gene]) == 0:
                    ans.add(gene)
    return ans


def getMutationSet() -> set:
    ans = set()
    for targetFolder in targetFolders:
        with open(os.path.join('data', targetFolder, '_mutation_%s.json' % targetGene)) as f:
            m = json.load(f)
            for gene in m:
                if len(m[gene]) != 0:
                    ans.add(gene)
    return ans


if __name__ == '__main__':
    a = getNoneMutationSet()
    b = getMutationSet()
