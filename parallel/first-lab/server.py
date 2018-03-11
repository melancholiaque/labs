from settings import *

loop = get_event_loop()
slices, processed = deque(maxlen=COLS), deque(maxlen=COLS)
[slices.append(slc) for slc in range(COLS)]

async def serve(reader,writer):
    while slices:
        col_slice = slices.popleft()
        try:
            writer.write(dumps(col_slice).encode()+b'\n')
            await writer.drain()
            _ = await reader.readuntil()
            res = await reader.readuntil()
            print(f'column {col_slice} processed')
        except:
            slices.appendleft(col_slice)
            return
        processed.append(col_slice)
    if len(processed) == processed.maxlen:
        loop.stop()

async def terminate():
    loop.stop()

async def progress(reader,writer):
    writer.write(dumps(list(processed)).encode())
    await writer.drain()
    writer.write(b'end')
    await writer.drain()


async def handle_new_conn(reader, writer):
    msg = await reader.readuntil()
    msg = msg.decode().rstrip()
    action = {
        'client'    : partial(serve, reader, writer),
        'terminate' : terminate,
        'progress'  : partial(progress, reader, writer)
    }[msg]
    await action()

def server_run():
    coro = start_server(handle_new_conn, ADDR, PORT, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        print('server started')
        loop.run_forever()
    except KeyboardInterrupt:
        print('\nserver terminated')
    finally:
        server.close()
