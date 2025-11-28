"""
- Streams: High-level APIs for TCP, UDP, and SSL networking.
- Gather: Wait for multiple coroutines to complete.

Code example for `tcp_echo_client` from the official documentation.

We need to setup the `tcp_echo_server` to listen on port 8888 and wait for incoming connections.
"""
import asyncio


async def tcp_echo_client(message):
    await asyncio.sleep(1)
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print(f'Cliend sends: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Client received: {data.decode()!r}')

    print('Client close the connection')
    writer.close()
    await writer.wait_closed()

async def _handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Server received: {message!r} from {addr!r}")

    print(f"Server sends: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Server closes the connection")
    writer.close()
    await writer.wait_closed()

async def tcp_echo_server():
    server = await asyncio.start_server(
        _handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

async def main():
    await asyncio.gather(
        tcp_echo_server(),
        tcp_echo_client('Hello, world!')
    )

if __name__ == '__main__':
    asyncio.run(main())