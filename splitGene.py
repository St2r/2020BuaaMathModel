targetDir = 'data/2020-June'

end = {'TAG', 'TAA', 'TGA'}

ErrorFile = set()


def splitToJson(inputFile: str, outputFile: str):
    import json

    def judge(seq1: str, seq2: str) -> bool:
        level = 10
        count = 0
        try:
            for i in range(level):
                if seq1[i] != seq2[i]:
                    count += 1
            return count < 0.4 * level
        except IndexError:
            print('Index Error in ' + inputFile)
            ErrorFile.add(inputFile)
            return True

    content = ''
    output = {
        'gene': list()
    }
    with open(inputFile, 'r') as f:
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
                if (t_end > t_start + len(target['seq']) + 10):
                    break
                t_end += 3

            output['gene'].append({
                'name': target['name'],
                'seq': t[t_start: t_end]
            })
    with open(outputFile, 'w') as f:
        f.write(json.dumps(output, indent=1))


if __name__ == '__main__':
    import os

    inputFolder = '2020-June'
    outputFolder = inputFolder + '-Gene'
    if not os.path.isdir(os.path.join('data', outputFolder)):
        os.mkdir(os.path.join('data', outputFolder))

    for file in os.listdir(os.path.join('data', inputFolder)):
        inputFile = os.path.join('data', inputFolder, file)
        outputFile = os.path.join('data', outputFolder, file.replace('.txt', '.json'))
        print(inputFile + '_' + outputFile)
        splitToJson(inputFile, outputFile)
