# https://pymotw.com/3/asyncio/io_protocol.html

import asyncio
import logging
import sys

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


class EchoServer(asyncio.Protocol):

    def connection_made(self, transport):
        # transport is type of asyncio.Transport - abstraction for doing asynchronous I/O using the socket
        # triggered by each new connection
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger(
            'EchoServer_{}_{}'.format(*self.address)
        )
        self.log.debug('connection accepted')

    def data_received(self, data):
        # data is sent from client to server
        self.log.debug('received {!r}'.format(data))
        new_data = data + b' sending it back!'
        self.transport.write(new_data)
        self.log.debug('sent {!r}'.format(new_data))

    def eof_received(self):
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            self.log.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing')
        super().connection_lost(error)

# Create the server and let the loop finish the coroutine before
# starting the real event loop.

factory = event_loop.create_server(EchoServer, *SERVER_ADDRESS)
server = event_loop.run_until_complete(factory)
log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

# Another task to show server can do something else while waiting for IO
async def another_task():
    log = logging.getLogger('Another Task')
    i = 0
    while True:
        i += 1
        log.debug('Counting {}'.format(i))
        await asyncio.sleep(0.2) # Without an await this will never give up control and Server will not run!

event_loop.create_task(another_task())

# Enter the event loop permanently to handle all connection_lost
try:
    event_loop.run_forever()
finally:
    log.debug('closing server')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    log.debug('closing event loop')
    event_loop.close()
