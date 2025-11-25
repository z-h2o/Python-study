import random
import time


def log_function(func):
    def wrapper(*args, **kwargs):
        print("开始")
        result = func(*args, **kwargs)
        print("结束")
        return result

    return wrapper


@log_function
def add(a, b):
    print("执行add函数", a, b)
    return a + b


# add(1, 2)


# 带参数的装饰器
def retry(max_try=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_try):
                try:
                    print(f"尝试第 {i+1} 次")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第{i+1}次执行失败, 准备重试, 错误信息: {e}")
                    if i < max_try:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)
            else:
                raise e

        return wrapper

    return decorator


@retry(
    max_try=3,
)
def plus(a, b):
    """随机失败"""
    i = random.random()
    print(f"random.random() = {i}")
    if i >= 0.1:
        raise ValueError("随机失败")
    print("执行plus函数", a, b)
    return a * b


# n1 = random.randint(10, 100)
# n2 = random.randint(10, 100)
# try:
#     plus(n1, n2)
# except Exception as e:
#     print("所有尝试都失败了", e)


def singleton(cls):
    """单例装饰器"""
    instances = {}
    print("singleton装饰器初始化", instances, cls)

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


# 类装饰器
@singleton
class Database:
    def __init__(self):
        print("初始化数据库连接")

    def query(self, sql):
        print("执行查询", sql)
        return "查询结果"


d1 = Database()
d2 = Database()
d3 = Database()
# print(d1 == d2 == d3)

# d1.query("SELECT * FROM table")
# d2.query("SELECT * FROM table")
