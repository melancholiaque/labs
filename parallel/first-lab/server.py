from settings import COLS, PROGRESS, ADDR, PORT
from asyncio import get_event_loop, start_server
from json import dumps
from collections import deque
from functools import partial
from pickle import dump, load
from logging import basicConfig, info, INFO

basicConfig(filename='server.log', level=INFO)
loop = get_event_loop()
processed = deque(maxlen=COLS)
workers = 0

with open(PROGRESS, 'rb') as fp:
    slices = load(fp)

for i in range(COLS):
    if i not in slices:
        processed.append(i)


async def serve(reader, writer):
    global workers
    workers += 1
    info(f'new worker connected')
    while slices:
        column = slices.popleft()
        info(f'delegating column {column}')
        try:
            writer.write(dumps(column).encode()+b'\n')
            await writer.drain()
            _ = await reader.readuntil()
            res = await reader.readuntil()
            info(f'column {column} processed')
        except Exception:
            info(f'worker disconnected')
            slices.appendleft(column)
            info(f'column {column} returned to pull')
            workers -= 1
            return
        processed.append(column)
    if len(processed) == processed.maxlen:
        info('computational task completed')
        loop.stop()


async def terminate():
    loop.stop()


async def unknown_msg(msg):
    info(f'got unexpected message {msg}')


async def progress(reader, writer):
    writer.write(dumps({
            'workers': workers,
            'processed': list(processed)
    }).encode())
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
    }.get(msg, partial(unknown_msg, msg))
    await action()


def server_run():
    coro = start_server(handle_new_conn, ADDR, PORT, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        info('server started')
        loop.run_forever()
    except KeyboardInterrupt:
        info('server terminated by user')
    except Exception:
        info('server terminated unexpectedly')
    finally:
        with open(PROGRESS, 'wb') as fp:
            dump(slices, fp)
        info('progress saved')
        server.close()


if __name__ == '__main__':
    server_run()
