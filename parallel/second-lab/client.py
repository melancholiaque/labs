from dill import dumps
from itertools import count
from sys import argv

import asyncio
import aio_pika as apika

from settings import Q_NAME, SLOW, work_func


def wrap(f, *args, **kwargs):
    return (lambda: f(*args, **kwargs))


async def main(loop):

    prefix = argv[-1]

    conn = await apika.connect_robust(
        "amqp://guest:guest@localhost/", loop=loop
    )

    chan = await conn.channel()

    for i in count():
        await chan.default_exchange.publish(
            apika.Message(
                body=dumps(
                    wrap(work_func, prefix, i)
                )
            ),
            routing_key=Q_NAME
        )
        print(f' [x] sent fact of {i % 500}')
        if SLOW:
            await asyncio.sleep(1)

    await conn.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    except Exception:
        print('\ntask sending terminated')
    finally:
        loop.close()
