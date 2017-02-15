import asyncio

@asyncio.coroutine
def my_coroutine(future, task_name, secounds_to_sleep=3):
    print('{0} sleeping for: {1} seconds'.format(task_name, secounds_to_sleep))
    yield from asyncio.sleep(secounds_to_sleep)
    future.set_result('{0} is finished'.format(task_name))

def got_result(future):
    print('Future done: {0}'.format(future.result()))

loop = asyncio.get_event_loop()
future1 = asyncio.Future()
future2 = asyncio.Future()
future3 = asyncio.Future()

tasks = [
my_coroutine(future1, 'task1', 4),
my_coroutine(future2, 'task2', 3),
my_coroutine(future3, 'task3', 2),
]
future1.add_done_callback(got_result)
future2.add_done_callback(got_result)
future3.add_done_callback(got_result)

loop.run_until_complete(asyncio.wait(tasks))
loop.close()
