# Introduction

This is a repository with exercises to understand Python asyncio (Asynchronous I/O) package.

# Prerequisites

- Python 3.13.2

# Topics

## Exercise 1: Coroutines

- Coroutines: Special functions declared with async def that can pause and resume execution.
- Async/Await: Keywords to define and manage asynchronous operations, making code look synchronous but run asynchronously.

## Exercise 2: Tasks

- Tasks: Special objects that can be used to manage asynchronous operations.

As defined by the official documentation:

> A Future-like object that runs a Python coroutine. Not thread-safe. 

> Tasks are used to run coroutines in event loops. If a coroutine awaits on a Future, the Task suspends the execution of the coroutine and waits for the completion of the Future. When the Future is done, the execution of the wrapped coroutine resumes.

## Exercise 3: Streams

- Streams: High-level APIs for TCP, UDP, and SSL networking. Streams allow sending and receiving data without using callbacks or low-level protocols and transports.
- Gather: Wait for multiple coroutines to complete. This enables you to run multiple coroutines concurrently.

```python
reader, writer = await asyncio.open_connection('example.com', 80)
```

## Exercise 4: Subprocesses

- Subprocess: Spawning a new process under the control of the event loop.

## Exercise 5: Queues

## Exercise 6: Exceptions