import asyncio

async def f():
    loop_1 = asyncio.get_running_loop()
    loop_2 = asyncio.get_running_loop()
    print(loop_1 is loop_2)

asyncio.run(f())