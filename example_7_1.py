import asyncio


class OneAtATime:
    def __init__(self, keys: list[str]):
        self.keys = keys
    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self
    async def __anext__(self):
        try:
            await asyncio.sleep(1)
            return next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration
        

async def main():
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    async for it in OneAtATime(keys):
        print(it)

asyncio.run(main())