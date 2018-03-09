from settings import *

loop = get_event_loop()
slices, processed = Queue(COLS), Queue(COLS)
[slices.put_nowait(slc) for slc in range(COLS)]

async def handle_new_conn(reader, writer):
    col_slice = await slices.get()
    writer.write(dumps(col_slice).encode()+b'\n')
    await writer.drain()
    res = await reader.readuntil()
    writer.close()
    await processed.put(res)
    if processed.full():
        loop.stop()

coro = start_server(handle_new_conn, ADDR, PORT, loop=loop)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
finally:
    server.close()
