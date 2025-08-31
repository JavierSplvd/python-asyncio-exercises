"""
- Queues: Asynchronous FIFO queues for producer-consumer patterns.
"""

import asyncio
import random

queue = asyncio.Queue(maxsize=3)

async def worker_sleep(index):
    random_time = random.randint(1, 5)
    await asyncio.sleep(random_time)
    print(f'Worker {index}, {random_time} seconds')

async def worker():
    while True:
        task = await queue.get()
        try:
            await task
        finally:
            queue.task_done()

async def main():
    workers = [asyncio.create_task(worker()) for _ in range(3)]
    
    for i in range(3):
        task = worker_sleep(i)
        await queue.put(task)

    await queue.join()

    # Cancel worker tasks to stop the event loop and exit
    for w in workers:
        w.cancel()

if __name__ == '__main__':
    asyncio.run(main())