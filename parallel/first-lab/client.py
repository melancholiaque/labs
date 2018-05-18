from settings import ADDR, PORT, FNAME1, FNAME2, ROWS
from asyncio import open_connection, get_event_loop
from json import loads
from time import time
from sys import argv

from numpy import genfromtxt, dot, fromstring
from tqdm import tqdm


verbose = argv[-1] != '-q'


async def mapper(loop):
    reader, writer = await open_connection(ADDR, PORT, loop=loop)
    writer.write(b'client\n')
    await writer.drain()
    while True:
        writer.write(b'ready\n')
        await writer.drain()
        data = await reader.readuntil()
        col_num, result = loads(data.decode().rstrip()), []
        if verbose:
            print(f'acquiring column {col_num}')
        beg = time()
        col = genfromtxt(FNAME2, delimiter=',', usecols=(col_num,))
        end = time()
        if verbose:
            print(f"column acquired for {end - beg} sec, multiplying")
        with open(FNAME1, 'r') as fp:
            efp = enumerate(fp)
            for n, l in verbose and tqdm(efp, total=ROWS) or efp:
                row = fromstring(l, sep=',')
                result.append(dot(row, col))
        with open(f'cols/{col_num}.dat', 'w') as fp:
            fp.write(f"{','.join(map(str, result))}\n")
        writer.write(b'processed\n')
        await writer.drain()
    writer.close()

loop = get_event_loop()
try:
    loop.run_until_complete(mapper(loop))
except KeyboardInterrupt:
    if verbose:
        print('\ncomputation terminated')
except Exception as e:
    if verbose:
        print('error occured during connection or computation')
        print(e)
finally:
    loop.close()
