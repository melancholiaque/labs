from settings import *
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)
loop = get_event_loop()
processed = deque(maxlen=COLS)
workers = 0
with open('progress.dat', 'rb') as fp:
    slices = load(fp)

for i in range(COLS):
    if not i in slices:
        processed.append(i)

async def serve(reader,writer):
    global workers
    workers += 1
    logging.info(f'new worker connected')
    while slices:
        col_slice = slices.popleft()
        logging.info(f'delegating col {col_slice}')
        try:
            writer.write(dumps(col_slice).encode()+b'\n')
            await writer.drain()
            _ = await reader.readuntil()
            res = await reader.readuntil()
            logging.info(f'col {col_slice} processed')
        except:
            logging.info(f'worker disconnected')
            slices.appendleft(col_slice)
            logging.info(f'col {col_slice} returned to pull')
            workers -= 1
            return
        processed.append(col_slice)
    if len(processed) == processed.maxlen:
        logging.info('computational task completed')
        loop.stop()

async def terminate():
    loop.stop()

async def progress(reader,writer):
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
    }[msg]
    await action()

def server_run():
    coro = start_server(handle_new_conn, ADDR, PORT, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        logging.info('server started')
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('server terminated by user')
    except:
        logging.info('server terminated unexpectedly')
    finally:
        with open('progress.dat', 'wb') as fp:
            dump(slices, fp)
        logging.info('progress saved')
        server.close()

if __name__ == '__main__':
    server_run()
