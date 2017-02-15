# asyncio

https://pymotw.com/3/asyncio/index.html
https://www.youtube.com/watch?v=N4YjNKSQVAI&t=1536s

* application code has to explicitly handle context changes

## Event Loop

* there are implementations for different operation systems
* application has to register code to be run_forever (this code can yield back control to event loop => Coroutine)
* can schedule calls to regular functions based on the timer value kept in the loop (asyncio_call_soon.py)

## Coroutine

* special functions that give up control to the caller *without losing their state*
* similar to generator functions
* language construct
* a coroutine function creates a coroutine object when called and the caller can run the code of the function using the coroutine's `send()` method
* can pause execution using the `await` keyword with another coroutine
* See [PEP-0492](https://www.python.org/dev/peps/pep-0492/#new-coroutine-declaration-syntax) for syntax

```python
async def coroutine():
  print ('hello world')
```

## Generators

* can be used to implement coroutines in versions of Python earlier than 3.5 (without native support for coroutine objects)
* instead of `async def` and `await` use `asyncio.coroutine()` decorator and `yield from` to achieve the same effect
* `yield from` [new in python 3.3](http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html)
   * to call a generator from a generator and yield its value
   * to refactore generators
   * give control to event loop until this is done


### Basics

* https://wiki.python.org/moin/Generators
* behave like an iterator / are a special kind of iterator
* convenient shortcut to building iterators that consume less ram
* `yield` like `return` but save state of function and restart execution from there
* shortcut to build generators:

``` python
# list comprehension
doubles = [2 * n for n in range(5000000)]
# generator comprehension
doubles = (2 * n for n in range(5000000))
```

## Future

* working like a coroutine
* data structure representing the result of work that has not been completed yet
* event loop can watch for a `Future` object to be set to done
* one part of an application can wait for another part to finish some work
* can invoke callbacks when it is completed


### Task

* subclass of `Future`
* wraps and manages the execution for a coroutine
* can be scheduled with the event loop to run when the resources they need are available and to produce a result that can be consumed by other coroutines
