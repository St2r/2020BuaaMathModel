import minDistance
import os
import json

targetFolder = '2020-March-Gene'
targetGene = 'M'

if __name__ == '__main__':
    with open('data/refTargetSeq.json', 'r') as f:
        for g in json.load(f)['gene']:
            if g['name'] == targetGene:
                refSeq = g['seq']

    output = dict()

    count = 0
    for file in os.listdir(os.path.join('data', targetFolder)):
        if file[0] == '_':
            continue
        else:
            with open(os.path.join('data', targetFolder, file), 'r') as f:
                for g in json.load(f)['gene']:
                    if g['name'] == targetGene:
                        targetSeq = g['seq']
            output[file.replace('.json', '')] = list()
            minDistance.backtrackingPath(refSeq, targetSeq, output[file.replace('.json', '')])
            # if len(output[file]) != 0:
            #     i = 1
        count += 1
        if count % 50 == 0:
            print(count)

    with open(os.path.join('data', targetFolder, '_mutation_%s.json' % targetGene), 'w') as f:
        f.write(json.dumps(output, indent=1))
