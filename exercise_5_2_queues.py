"""
"""

import asyncio

transaction_queue = asyncio.Queue(maxsize=5)

async def random_sleep_coroutine(index):
    random_time = random.randint(1, 5)
    await asyncio.sleep(random_time)
    print(f'Worker #{index}, {random_time} seconds')

async def transaction():
    while True:
        worker_index = await transaction_queue.get()
        try:
            await random_sleep_coroutine(worker_index)
        finally:
            transaction_queue.task_done()

async def main():
    workers = []
    for worker_id in range(30):
        await transaction_queue.put(worker_id)
        workers.append(asyncio.create_task(transaction()))
        await asyncio.sleep(1)

    await transaction_queue.join()

    # Cancel worker tasks to stop the event loop and exit
    for w in workers:
        w.cancel()

if __name__ == '__main__':
    asyncio.run(main())