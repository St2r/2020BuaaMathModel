class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        if len(word2) < len(word1):  # 保证word1是短单词
            word1, word2 = word2, word1
        m, n = len(word1), len(word2)
        dist = list(range(m + 1))  # word2长度为0时，由不同长度word1转换的编辑距离
        for i in range(1, n + 1):
            tmp = [i] * (m + 1)  # word2长度为i时，由0长度的word1转换的编辑距离
            for j in range(1, m + 1):
                if word1[j - 1] == word2[i - 1]:
                    tmp[j] = dist[j - 1]
                else:
                    tmp[j] = min(tmp[j - 1], dist[j], dist[j - 1]) + 1
            dist = tmp
        return dist[-1]


if __name__ == '__main__':
    import os

    files = os.listdir('mini')
    with open('output.txt', 'w') as out:
        cur = 1
        for file in files:
            print('>test%d' % cur, file=out)
            with open('mini/' + file, 'r') as f:
                for line in f.readlines():
                    print(line.strip().replace('\n', ''), file=out)
            cur += 1
