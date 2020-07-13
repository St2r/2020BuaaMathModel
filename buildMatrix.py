import numpy as np
import minDistance
import json
import os
import sumNoneMutation

class ConnectMatrix:
    def __init__(self, seq: str):
        self.geneList = [['ref-NC045512', seq, 1]]
        self.matrix = np.array([[0]])

    def addGene(self, name: str, seq: str):
        cache = np.zeros(len(self.matrix) + 1)
        cur_index = 0
        for gene in self.geneList:
            dis = minDistance.minDistance(gene[1], seq)[-1][-1]
            if dis == 0:
                gene[2] += 1
                return
            cache[cur_index] = dis
            cur_index += 1
        self.geneList.append([name, seq, 1])
        self.matrix = np.insert(self.matrix, len(self.matrix), values=cache[:-1], axis=1)
        self.matrix = np.insert(self.matrix, len(self.matrix), values=cache, axis=0)


if __name__ == '__main__':
    targetGene = 'M'

    mutation = sumNoneMutation.getMutationSet()

    with open(os.path.join('data', 'refTargetSeq.json'), 'r') as f:
        genes = json.load(f)['gene']
        for gene in genes:
            if gene['name'] == targetGene:
                c = ConnectMatrix(gene['seq'])
                break

    count = 0
    count_mutation = 0
    with open(os.path.join('data', 'summary_gene_%s.json' % targetGene), 'r') as f:
        genes = json.load(f)
        for name in genes:
            if name in mutation:
                c.addGene(name, genes[name])
                count_mutation += 1
                print('Add %d Gene To Graph' % count_mutation)
            count += 1
            if count % 10 == 0:
                print(count)

    with open('ouput.json', 'w') as f:
        f.write(json.dumps({
            'geneList': c.geneList,
            'matrix': c.matrix.tolist()
        }, indent=1))
