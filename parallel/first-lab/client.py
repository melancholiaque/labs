from settings import *

async def mapper(loop):
    reader, writer = await open_connection(ADDR, PORT, loop=loop)
    data = await reader.readuntil()
    col_num, result = loads(data.decode().rstrip()), []
    col = genfromtxt(FNAME, delimiter=',', usecols=(col_num,))
    with open('file','r') as fp:
        for l in fp:
            result.append(dot(fromstring(l, dtype=int32, sep=','), col))
    with open(f'cols/{col_num}','w') as fp:
        fp.write(f"{','.join(map(str, result))}\n")
    writer.write(b'processed\n')
    await writer.drain()
    writer.close()

loop = get_event_loop()
loop.run_until_complete(mapper(loop)) and loop.close()
