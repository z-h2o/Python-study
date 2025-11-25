import time
import asyncio
from venv import create


# 测试同步阻塞的time.sleep
def test_sync_sleep():
    print("=== 测试同步time.sleep ===")
    start = time.time()

    print(f"开始时间: {time.time() - start:.2f}秒")
    time.sleep(2)
    print(f"第一次sleep后: {time.time() - start:.2f}秒")
    time.sleep(2)
    print(f"第二次sleep后: {time.time() - start:.2f}秒")

    print(f"总共耗时: {time.time() - start:.2f}秒")


# 异步测试asyncio.sleep
async def async_task(name, delay=1):
    print(f"任务{name}开始")
    await asyncio.sleep(delay)  # 非阻塞等待
    print(f"任务{name}结束")
    return f"任务{name}完成"


async def test_async_sleep():
    print("\n=== 测试异步asyncio.sleep ===")
    start = time.time()

    # 创建两个协程任务
    task1 = asyncio.create_task(async_task("A", 1))
    task2 = asyncio.create_task(async_task("B", 2))

    # await asyncio.sleep(6)
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2)

    print(f"\n所有任务完成: {results}")
    print(f"总共耗时: {time.time() - start:.2f}秒")


# 主函数
if __name__ == "__main__":
    asyncio.run(test_async_sleep())
    test_sync_sleep()
