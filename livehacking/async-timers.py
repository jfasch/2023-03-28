import asyncio

async def blink(on, off, delay, n):
    for _ in range(n):
        print(on)
        await asyncio.sleep(delay)
        print(off)

async def main():
    task1 = asyncio.create_task(blink('on1', 'off1', 0.2, 100))
    task2 = asyncio.create_task(blink('on2', 'off2', 0.5, 50))

    await task1
    await task2

asyncio.run(main())
