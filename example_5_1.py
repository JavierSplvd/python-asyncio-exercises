import asyncio

async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    f.set_result("Hello world")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

fut: asyncio.Future = asyncio.Future()
print(fut.done())

loop.create_task(main(fut))
loop.run_until_complete(fut)
print(fut.done())
print(fut.result())

loop.close()