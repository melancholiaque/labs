from settings import *

async def mapper(loop):
    reader, writer = await open_connection(ADDR, PORT, loop=loop)
    data = await reader.readuntil()
    '''result = defaultdict(int)
    async with aiofiles.open(data.decode().rstrip(),'r') as f:
        async for line in f:
            for word in line.rstrip().split():
                result[word.lower()] += 1
    writer.write(f'{dumps(result[WORD])}\n'.encode())'''
    sleep(10)
    writer.write('0\n'.encode())
    await writer.drain()
    writer.close()

loop = get_event_loop()
loop.run_until_complete(mapper(loop)) and loop.close()
