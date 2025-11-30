import asyncio

async def foo():
    print("foo started")
    await asyncio.sleep(3)
    print("foo resumed")

async def old_way():
    loop = asyncio.get_running_loop()
    for i in range(3):
        loop.create_task(foo())

async def new_way():
    for i in range(3):
        asyncio.create_task(foo())


async def main():
    await new_way()
    await old_way()
    await asyncio.sleep(4)

asyncio.run(main())