import asyncio
from typing import AsyncGenerator


async def one_at_a_time(keys: list[str]) -> AsyncGenerator[str]:
    for k in keys:
        await asyncio.sleep(1)
        yield k

print(one_at_a_time)
print(one_at_a_time([]))

async def main():
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    async for it in one_at_a_time(keys):
        print(it)

asyncio.run(main())