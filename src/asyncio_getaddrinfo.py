# https://pymotw.com/3/asyncio/dns.html

import asyncio
import logging
import socket
import sys


TARGETS = [
    ('pymotw.com', 'https'),
    ('doughellmann.com', 'https'),
    ('python.org', 'https'),
    ('uni-marburg.de', 'https')
]

async def count():
    i = 0
    while i < 20:
        print(i)
        await asyncio.sleep(0.001)
        i += 1


async def main(loop, targets):
    task = loop.create_task(count())

    for target in targets:
        info = await loop.getaddrinfo(*target, proto=socket.IPPROTO_TCP)
        for host in info:
            print('{:20}: {}'.format(target[0], host[4][0]))

    await asyncio.wait([task,])

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, TARGETS))
finally:
    event_loop.close()