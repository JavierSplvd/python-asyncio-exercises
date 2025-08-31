"""
In this exercise, you will learn about:
Coroutines: Special functions declared with async def that can pause and resume execution.
Async/Await: Keywords to define and manage asynchronous operations, making code look synchronous but run asynchronously.

We will create two coroutines and run them sequentially, coroutine1 will run first and once finished, coroutine2 will run.
"""

import asyncio


async def coroutine1():
    print("Coroutine 1")
    await asyncio.sleep(3)
    print("Coroutine 1 resumed")


async def coroutine2():
    print("Coroutine 2")
    await asyncio.sleep(1)
    print("Coroutine 2 resumed")

async def main():
    await coroutine1()
    await coroutine2()

if __name__ == "__main__":
    asyncio.run(main())