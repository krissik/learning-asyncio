# http://www.giantflyingsaucer.com/blog/?p=5557
import asyncio

@asyncio.coroutine
def my_coroutine(secounds_to_sleep=3):
    print('my_coroutine sleeping for: {0} seconds'.format(secounds_to_sleep))
    yield from asyncio.sleep(secounds_to_sleep)

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(my_coroutine())
)
loop.close()
