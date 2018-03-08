from asyncio import open_connection, get_event_loop, Queue, start_server
from json import dumps, loads
from collections import defaultdict
from time import sleep
from os import listdir, path
import aiofiles

ADDR, PORT, DATADIR, WORD  = '127.0.0.1', 8764, 'data', 'он'
FILES = [f'{path.join(DATADIR, f)}\n' for f in listdir(DATADIR)]
