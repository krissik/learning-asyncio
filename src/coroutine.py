# https://pymotw.com/3/asyncio/coroutines.html

import asyncio

async def coroutine():
    print('in coroutine')
    return 'a return value'

event_loop = asyncio.get_event_loop()
try:
    print('starting coroutine')
    coro = coroutine()
    print('entering event loop')
    result = event_loop.run_until_complete(coro)
    print('Corotine has result "{0}"'.format(result))
finally:
    print('closing event loop')
    event_loop.close()
