from asyncio import open_connection, get_event_loop, Queue, start_server
from json import dumps, loads
from collections import defaultdict
from os import listdir, path
from numpy import genfromtxt, dot, fromstring, int32

ADDR, PORT, FNAME = '127.0.0.1', 8764, 'file'
ROWS, COLS = 100, 100
COLS_SLICES = 5
ROW_SLICES = COLS_SLICES
