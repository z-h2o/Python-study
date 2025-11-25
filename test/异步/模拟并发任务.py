import asyncio
import random


async def get_user_info_by_id(user_id):
    try:
        time = 0.5 + random.random()
        await asyncio.sleep(time)
        return {"user_id": user_id, "name": f"user_{user_id}"}
    except Exception as e:
        print(f"获取用户{user_id}信息失败, 错误信息: {e}")
        return None


async def get_all_user():
    user_ids = [1001, 1002, 1003, 1004, 1005]
    tasks = [get_user_info_by_id(user_id) for user_id in user_ids]
    task_res = await asyncio.gather(*tasks)
    print("并发获取所有任务的数据==>", task_res)
    return task_res


asyncio.run(get_all_user())

print("\n\n")


async def get_first_user():
    user_ids = [1001, 1002, 1003, 1004, 1005]
    tasks = [asyncio.create_task(get_user_info_by_id(user_id)) for user_id in user_ids]
    done, padding = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # 获取已完成任务的结果
    res = done.pop().result()
    print("第一个完成的任务==>", res)
    # 取消未完成任务
    for task in padding:
        task.cancel()
    return res


asyncio.run(get_first_user())
