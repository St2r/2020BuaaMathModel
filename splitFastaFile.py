import os
from typing import TextIO

if __name__ == '__main__':
    fileName = '2020-March'
    if not os.path.isdir(os.path.join('data', fileName)):
        os.mkdir(os.path.join('data', fileName))
    with open('data/%s.fasta' % fileName, 'r') as f:
        for line in f.readlines():
            target: TextIO
            if line[0] == '>':
                if 'target' in dir():
                    target.close()
                start = line.find(' ')
                target = open(os.path.join('data', fileName, line[1: start].replace('.', '_') + '.txt'), 'w')
            else:
                target.write(line)
