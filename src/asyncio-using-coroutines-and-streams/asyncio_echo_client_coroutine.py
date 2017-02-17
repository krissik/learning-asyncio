# https://pymotw.com/3/asyncio/io_coroutine.html#echo-clienthttps://pymotw.com/3/asyncio/io_coroutine.html#echo-client
# https://pymotw.com/3/asyncio/ssl.html

import asyncio
import logging
import ssl
import sys

MESSAGES = [
    b'This is the message ',
    b'It will be sent ',
    b'in parts.',
]

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


# is called when the task starts without active connections
async def echo_client(name, address, messages):
    log = logging.getLogger('echo_client_{}'.format(name))
    log.debug('connection to {} port {}'.format(*address))

    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH
    )
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('pymotw.crt')

    reader, writer = await asyncio.open_connection(*address, ssl=ssl_context)

    # This could be writer.writelines() except that
    # would make it harder to show each part of the message
    # being sent

    for msg in messages:
        msg_to_send = '\'{}\' from client {}'.format(msg.decode("utf-8"), name)
        msg_to_send = bytes(msg_to_send, encoding='UTF-8')
        writer.write(msg_to_send)
        log.debug('sending {!r}'.format(msg_to_send))

    writer.write(b'\x00')
    await writer.drain()

    log.debug('waiting for response')

    while True:
        data = await reader.read(512)
        if data:
            log.debug('received {!r}'.format(data))
        else:
            log.debug('closing')
            writer.close()
            return

try:
    # Run two clients
    # # one by one
    event_loop.run_until_complete(echo_client(' ### client 1 ### ', SERVER_ADDRESS, MESSAGES))
    log.debug(' ### client 1 ### completed')
    event_loop.run_until_complete(echo_client(' ### client 2 ### ', SERVER_ADDRESS, MESSAGES))
    log.debug(' ### client 2 ### completed')

    # # asynchronous
    task3 = event_loop.create_task(echo_client(' ### client 3 ### ', SERVER_ADDRESS, MESSAGES))
    task4 = event_loop.create_task(echo_client(' ### client 4 ### ', SERVER_ADDRESS, MESSAGES))
    event_loop.run_forever()
finally:
    log.debug('closing event loop')
    event_loop.close()
