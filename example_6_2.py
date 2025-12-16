import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def web_page(url):
    await asyncio.sleep(1)
    data = f"Hello world: {url}"
    yield data

async def main():
    async with web_page('google.com') as data:
        print(data)

asyncio.run(main())