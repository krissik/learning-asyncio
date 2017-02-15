# https://docs.python.org/3/library/asyncio-eventloop.html#event-loop-examples
import asyncio

def hello_world(loop):
    print('Hello World')
    loop.stop()

loop = asyncio.get_event_loop()
loop.call_soon(hello_world, loop)
print('before run_forever')
loop.run_forever()
print('after run_forever')
loop.close()
