import asyncio
import random
from random import randint
import requests

async def sleeper(name, seconds_to_sleep):
    # Do stupid blocking thing
    foo = requests.get('http://google.com')
    print(' Sleeping for {0}'.format(name))
    #await asyncio.sleep(seconds_to_sleep)
    print(' Sleeped for {0}'.format(name))

async def say_hello(name):
    print('Hello {0}'.format(name))
    sleep_time = random.randint(3, 5)
    await sleeper(name, sleep_time)
    print('Bye   {0}'.format(name))

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(say_hello('Earth'),
                    say_hello('World'),
                    say_hello('Universe'),
                    say_hello('Multiverse')
    )
)
