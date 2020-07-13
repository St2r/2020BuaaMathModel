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

if __name__ == '__main__':
    output = dict()
    for targetFolder in targetFolders:
        for file in os.listdir(os.path.join('data', targetFolder)):
            if file[0] == '_':
                continue
            else:
                with open(os.path.join('data', targetFolder, file), 'r') as f:
                    genes = json.load(f)['gene']
                    for gene in genes:
                        if gene['name'] == targetGene:
                            output[file.replace('.json', '')] = gene['seq']
    with open(os.path.join('data', 'summary_gene_%s.json' % targetGene), 'w') as f:
        f.write(json.dumps(output, indent=1))
