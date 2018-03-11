from asyncio import open_connection, get_event_loop, Queue, start_server
from json import dumps, loads
from collections import defaultdict, deque
from os import listdir, path
from numpy import genfromtxt, dot, fromstring, int32
from tqdm import tqdm
from time import time
from functools import partial

ADDR, PORT, FNAME1, FNAME2 = '127.0.0.1', 8764, 'file1.dat', 'file2.dat'
ROWS, COLS = 15_000, 15_000
COLS_SLICES = 5
ROW_SLICES = COLS_SLICES
