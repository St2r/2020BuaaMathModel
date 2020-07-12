import json

if __name__ == '__main__':
    with open('data/refSeq.json', 'r') as f:
        metadata = json.load(f)['targets']
    output = {
        'gene': list()
    }
    content = ''
    with open('data/refSeq.fasta', 'r') as f:
        for line in f.readlines()[1:]:
            content += line.strip().replace('\n', '')
    for target in metadata:
        sub_content = content[target['start'] - 1: target['end']]
        output['gene'].append({
            'name': target['name'],
            'start': target['start'],
            'end': target['end'],
            'length': target['end'] - target['start'] + 1,
            'seq': sub_content
        })
    with open('data/refTargetSeq.json', 'w') as f:
        f.write(json.dumps(output, indent=1))
