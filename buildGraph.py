from minSpanTree import Graph
import json


class GraphNode:
    def __init__(self, index: int, genes: list):
        self.index = index
        self.child = list()
        self.genes = genes

    def __str__(self) -> str:
        ans = self.genes[self.index][0][:-2] + '-%d-' % self.genes[self.index][2]
        if len(self.child) != 0:
            ans += '('
            ans += self.genes[self.index][0][:-2] + '-%d-' % self.genes[self.index][2]
            for j in range(0, len(self.child)):
                ans += ','
                ans += str(self.child[j])
            ans += ')'
        return ans

    def addNode(self, parent: int, child: int):
        if self.index == parent:
            self.child.append(GraphNode(child, self.genes))

        for c in self.child:
            c.addNode(parent, child)


if __name__ == '__main__':
    with open('ouput.json', 'r') as f:
        geneList = json.load(f)
        matrix = geneList['matrix']
        geneList = geneList['geneList']

    g = Graph(matrix)
    p = g.prim()
    root = GraphNode(0, geneList)
    for i in p:
        root.addNode(i[0], i[1])
    print(root)
