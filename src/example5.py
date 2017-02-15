import asyncio
import aiohttp

@asyncio.coroutine
def fetch_page(url, pause=False):
    if pause:
        yield from asyncio.sleep(2)
    response = yield from aiohttp.request('GET', url)
    assert response.status == 200
    content = yield from response.read()
    print ('URL: {0}: Content: {1}'.format(url, content[0:100]))

loop = asyncio.get_event_loop()

tasks = [
    fetch_page('http://google.com'),
    fetch_page('http://cnn.com', True),
    fetch_page('http://twitter.com')
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

for task in tasks:
    print(task)
