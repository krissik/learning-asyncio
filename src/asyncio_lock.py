# https://pymotw.com/3/asyncio/synchronization.html

import asyncio
import functools

def unlock(lock):
    print('callback releasing lock')
    lock.release()

async def coro1(lock):
    print('coro1 waiting for the lock')
    with await lock:
        print('coro1 acquired lock')
    print('coro1 released lock')

async def coro2(lock):
    print('coro2 waiting for the lock')
    await lock
    try:
        print('coro2 acquired lock')
    finally:
        print('coro2 released lock')
        lock.release()

async def main(loop):
    # Create an acquire a shared lock
    lock = asyncio.Lock()
    print('acquiring th lock before starting corotines')
    await lock.acquire()
    print('lock acquired: {}'.format(lock.locked()))
    # Schedule a callback to unlock the lock
    loop.call_later(0.1, functools.partial(unlock, lock))

    # Run the coroutines that want to use the lock
    print('waiting for coroutines')
    await asyncio.wait([coro1(lock), coro2(lock)])

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
