# https://pymotw.com/3/asyncio/control.html

"""
wait() can be used to pause one coroutine until th other background
operations complete - if order of execution doesn't matter.

"""

import asyncio

async def phase(i):
    print('in phase {}'.format(i))
    await asyncio.sleep(0.1 * i)
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)

async def main(num_phases):
    print('starting main')
    phases = [phase(i) for i in range(num_phases)]
    await asyncio.sleep(2) # Prove nothing will run yet
    print('waiting for phases to complete')
    completed, pending = await asyncio.wait(phases)
    results = [t.result() for t in completed]
    print('results: {!r}'.format(results))

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()
