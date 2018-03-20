from collections import defaultdict
from os import listdir, path

result = defaultdict(int)
DATADIR = 'data'
WORD = 'он'
FILES = [f'{path.join(DATADIR, f)}' for f in listdir(DATADIR)]

for file_ in FILES:
    with open(file_, 'r') as f:
        for line in f:
            for word in line.rstrip().split():
                result[word.lower()] += 1


                
print(f'word <<{WORD}>> appeared {result[WORD]} times')
