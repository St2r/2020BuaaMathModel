targetDir = 'data/2020-June'

end = {'TAG', 'TAA', 'TGA'}

ErrorFile = set()


def splitToJson(inputFile: str, outputFile: str):
    import json

    def judge(seq1: str, seq2: str, start: int, end: int) -> bool:
        if end - start < 50:
            return False
        count = 0

        for i in range(25):
            if seq1[i] != seq2[start + i]:
                count += 1
        for i in range(25):
            if seq1[-i] != seq2[end - i]:
                count += 1
        return count < 10

    content = ''
    output = {
        'gene': list()
    }
    with open(inputFile, 'r') as f:
        for line in f.readlines():
            content += line.strip().replace('\n', '')
    with open('data/refTargetSeq.json') as f:
        t_start = -1
        for target in json.load(f)['gene']:

            while True:
                t_start = content.find('ATG', t_start + 1)

                if t_start == -1:
                    ErrorFile.add(inputFile)
                    return;

                t_end = t_start + 3
                while content[t_end - 3: t_end] not in end:
                    if t_end > len(content):
                        break
                    t_end += 3
                if judge(target['seq'], content, t_start, t_end):
                    break;

            output['gene'].append({
                'name': target['name'],
                'start': t_start,
                'length': t_end - t_start,
                'seq': content[t_start: t_end]
            })

    with open(outputFile, 'w') as f:
        f.write(json.dumps(output, indent=1))


if __name__ == '__main__':
    import os
    import json

    inputFolder = '2020-June'
    outputFolder = inputFolder + '-Gene'
    if not os.path.isdir(os.path.join('data', outputFolder)):
        os.mkdir(os.path.join('data', outputFolder))

    count = 0
    for file in os.listdir(os.path.join('data', inputFolder)):
        inputFile = os.path.join('data', inputFolder, file)
        outputFile = os.path.join('data', outputFolder, file.replace('.txt', '.json'))
        count += 1
        print(str(count) + '_' + inputFile)
        splitToJson(inputFile, outputFile)

    output = {
        'error': list()
    }
    for e in ErrorFile:
        output['error'].append({
            'filename': e
        })
    with open(os.path.join(outputFolder, '_error_file.json')) as f:
        f.write(json.dumps(output, indent=1))