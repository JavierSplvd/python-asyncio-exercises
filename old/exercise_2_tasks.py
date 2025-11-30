"""
- Tasks: Special objects that can be used to manage asynchronous operations.

The API offers `asyncio.create_task()` and `asyncio.TaskGroup()` to create tasks. The TaskGroup offers a context manager to hold a group of tasks that will be awaited when the context manager is exited.
"""
import asyncio


async def task1():
    print("Task 1")
    await asyncio.sleep(1)
    print("Task 1 resumed")

async def main():
    task_1 = asyncio.create_task(task1())
    await task_1

async def main_with_task_group():
    async with asyncio.TaskGroup() as tg:
        task_1 = tg.create_task(task1())

if __name__ == "__main__":
    asyncio.run(main())
    print("---")
    asyncio.run(main_with_task_group())