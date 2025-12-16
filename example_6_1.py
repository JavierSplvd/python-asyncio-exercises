import asyncio
from contextlib import asynccontextmanager


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def __aenter__(self):
        await asyncio.sleep(1)
        return "Hello world from connection"

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(1)


async def connection_example():
    async with Connection('localhost', 9001) as conn:
        print(conn)
        pass

asyncio.run(connection_example())
