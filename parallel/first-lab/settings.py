from os import path
from collections import deque
from pickle import dump

ADDR, PORT = '127.0.0.1', 8764
FNAME1, FNAME2 = 'matrixes/A.dat', 'matrixes/B.dat'
PROGRESS = 'progress.dat'
ROWS, COLS = 1_000, 1_000

if not path.exists(PROGRESS):
    with open(PROGRESS,'wb') as fp:
        dump(deque(iterable=list(range(COLS)), maxlen=COLS), fp)
    
