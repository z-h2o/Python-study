import asyncio


async def sync_task():
    print("异步任务开始=>")
    await asyncio.sleep(1)
    print("异步任务完成=>")


async def main():
    print("1. 开始")
    task1 = asyncio.create_task(sync_task())
    task2 = asyncio.create_task(asyncio.sleep(4))

    await task1
    print("2. 任务1完成")
    await task2
    print("3. 任务2完成")


asyncio.run(main())
