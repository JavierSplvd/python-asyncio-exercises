"""
- Queues: Asynchronous FIFO queues for producer-consumer patterns.

In this exercise we combine different concepts. We will create a queue with the id of the workers. Each worker will sleep for a random amount of time and then finish.

We use `create_task()` to create a task for each worker. We use `get()` to get the id of the worker and `task_done()` to signal that the worker is done.

The `join()` method is used to wait for all the workers to finish, they will finish when the queue is empty.
"""

import asyncio
import random

queue = asyncio.Queue(maxsize=3)

async def random_sleep_coroutine(index):
    random_time = random.randint(1, 5)
    await asyncio.sleep(random_time)
    print(f'Worker #{index}, {random_time} seconds')

async def worker():
    while True:
        worker_index = await queue.get()
        try:
            await random_sleep_coroutine(worker_index)
        finally:
            queue.task_done()

async def main():
    workers = [asyncio.create_task(worker()) for _ in range(3)]

    for worker_id in range(3):
        await queue.put(worker_id)

    await queue.join()

    # Cancel worker tasks to stop the event loop and exit
    for w in workers:
        w.cancel()

if __name__ == '__main__':
    asyncio.run(main())