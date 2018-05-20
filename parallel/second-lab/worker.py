from dill import loads
from sys import argv
import asyncio
import aio_pika as apika

from settings import Q_NAME


def wrap(f, *args, **kwargs):
    return (lambda: f(*args, **kwargs))


async def process(loop):

    prefix = argv[-1]

    conn = await apika.connect_robust(
        "amqp://guest:guest@localhost/", loop=loop
    )

    async with conn:
        chan = await conn.channel()
        queue = await chan.declare_queue(Q_NAME)
        await chan.set_qos(prefetch_count=1)

        async for message in queue:
            with message.process():
                res = loads(message.body)()
                print(f'[worker {prefix}] [{res}]')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(process(loop))
    except Exception as e:
        print(e)
        print('\ntask sending terminated')
    finally:
        loop.close()
