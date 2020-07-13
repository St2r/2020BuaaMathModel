def minDistance(word1, word2):
    if len(word1) == 0:
        return len(word2)
    elif len(word2) == 0:
        return len(word1)
    M = len(word1)
    N = len(word2)
    output = [[0] * (N + 1) for _ in range(M + 1)]
    for i in range(M + 1):
        for j in range(N + 1):
            if i == 0 and j == 0:
                output[i][j] = 0
            elif i == 0 and j != 0:
                output[i][j] = j
            elif i != 0 and j == 0:
                output[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                output[i][j] = output[i - 1][j - 1]
            else:
                # 增删和替换代价比为10
                output[i][j] = min(output[i - 1][j - 1] + 1, output[i - 1][j] + 10, output[i][j - 1] + 10)
    return output


def backtrackingPath(word1, word2, record: list):
    dp = minDistance(word1, word2)
    m = len(dp) - 1
    n = len(dp[0]) - 1

    while n >= 0 or m >= 0:
        if n and dp[m][n - 1] + 1 == dp[m][n]:
            # print("insert %c" % (word2[n - 1]) + ' at ' + str(m) + '\n')
            record.append({
                'type': 'insert',
                'position': m,
                'target': word2[n-1]
            })
            n -= 1
            continue
        if m and dp[m - 1][n] + 1 == dp[m][n]:
            # print("delete %c\n" % (word1[m - 1]) + ' at ' + str(m) + '\n')
            record.append({
                'type': 'delete',
                'position': m,
                'target': word1[m-1]
            })
            m -= 1
            continue
        if dp[m - 1][n - 1] + 1 == dp[m][n]:
            # print("replace %c to %c" % (word1[m - 1], word2[n - 1]) + ' at ' + str(m) + '\n')
            record.append({
                'type': 'replace',
                'position': m,
                'source': word1[m-1],
                'target': word2[n-1]
            })
            n -= 1
            m -= 1
            continue
        if dp[m - 1][n - 1] == dp[m][n]:
            pass
        n -= 1
        m -= 1


if __name__ == '__main__':
    l = list()
    backtrackingPath('AAA', 'ACA', l)
