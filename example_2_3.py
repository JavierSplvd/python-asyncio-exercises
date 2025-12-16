import time
import asyncio

async def first_use_case():
	print(f'{time.ctime()} Hello!')
	await asyncio.sleep(1.0)
	print(f'{time.ctime()} Goodbye!')

def second_use_case():
	time.sleep(0.5)
	print(f"{time.ctime()} Hello from a thread!")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(first_use_case())

loop.run_in_executor(None, second_use_case)
loop.run_until_complete(task)

pending = asyncio.all_tasks(loop=loop)
for task in pending:
	task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()