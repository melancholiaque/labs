from settings import FNAME1, FNAME2, ADDR, PORT, ROWS, COLS
import socket

import numpy as np
from tqdm import tqdm

def gen_sample():
    for FILE in (FNAME1, FNAME2):
        with open(FILE,'w') as fp:
            for i in tqdm(range(ROWS)):
                rand_range = np.random.rand(COLS)
                fp.write(f"{','.join(map(str, rand_range))}\n")
                del rand_range

def send(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR, PORT))
    s.send(msg.encode() + b'\n')
    s.close()

def send_return(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR,PORT))
    s.send(msg.encode() + b'\n')
    result = ''
    chunk = s.recv(1024)
    while chunk:
        if b'end' in chunk:
            result += chunk.decode().rstrip('end')
            s.close()
            return result
        else:
            result += chunk.decode()
        chunk = s.recv(4096)
