# https://pymotw.com/3/asyncio/io_coroutine.html
# https://pymotw.com/3/asyncio/ssl.html

import asyncio
import logging
import ssl
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
        terminate = data.endswith(b'\x00')
        data = data.rstrip(b'\x00')
        if data:
            log.debug('received {!r}'.format(data))
            writer.write(data)
            await writer.drain()  # flush non blocking
            log.debug('sent {!r}'.format(data))
        if not data or terminate:
            log.debug('message terminated, closing connection')
            writer.close()
            return


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain('pymotw.crt', 'pymotw.key')

# Create the server and let the loop finish the coroutine before
# starting the real event loop.

factory = asyncio.start_server(echo, *SERVER_ADDRESS, ssl=ssl_context)
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
