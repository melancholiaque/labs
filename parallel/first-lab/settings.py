from asyncio import open_connection, get_event_loop, Queue, start_server
from json import dumps, loads
from collections import defaultdict, deque
from os import listdir, path
from numpy import genfromtxt, dot, fromstring, int32
from tqdm import tqdm
from time import time
from functools import partial
from pickle import dump, load

ADDR, PORT = '127.0.0.1', 8764
FNAME1, FNAME2 = 'matrixes/file1.dat', 'matrixes/file2.dat'
PROGRESS = 'progress.dat'
ROWS, COLS = 1000, 1000
COLS_SLICES = 5
ROW_SLICES = COLS_SLICES

if not path.exists(PROGRESS):
    with open(PROGRESS,'wb') as fp:
        dump(deque(iterable=list(range(COLS)), maxlen=COLS), fp)
    
