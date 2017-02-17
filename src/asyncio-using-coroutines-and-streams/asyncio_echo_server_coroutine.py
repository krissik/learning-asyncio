# https://pymotw.com/3/asyncio/io_coroutine.html

import asyncio
import logging
import sys

SERVER_ADDRESS = ('localhost', 10000)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s:#: %(message)s',
    stream=sys.stderr
)

log = logging.getLogger('main')
event_loop = asyncio.get_event_loop()


# each time a client connects, a new instance of this coroutine
# will be invoked
async def echo(reader, writer):
    address = writer.get_extra_info('peername')
    log = logging.getLogger('echo_{}_{}'.format(*address))
    log.debug('connection accepted')

    while True:
        data = await reader.read(128)  # non blocking read
        if data:
            log.debug('received {!r}'.format(data))
            writer.write(data)
            await writer.drain()  # flush non blocking
            log.debug('sent {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return


# Create the server and let the loop finish the coroutine before
# starting the real event loop.

factory = asyncio.start_server(echo, *SERVER_ADDRESS)
server = event_loop.run_until_complete(factory)
log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

try:
    event_loop.run_forever()
except KeyboardInterrupt:
    log.debug('KeyboardInterrupt')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    log.debug('closing event loop')
    event_loop.close()
