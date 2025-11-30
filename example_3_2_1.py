import asyncio


class MyClass:
    def __await__(self):
        for i in range(3):
            print(i)
            yield from asyncio.sleep(i).__await__()
        return self


async def main():
    r = await MyClass()
    print(r)
    return r

asyncio.run(main())