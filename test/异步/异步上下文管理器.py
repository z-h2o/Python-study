import asyncio
from contextlib import asynccontextmanager


# =============================================================================
# 异步上下文管理器示例
# 异步上下文管理器允许在异步代码中使用 async with 语句，用于资源的异步获取和释放
# =============================================================================


# 方法1：通过类实现异步上下文管理器
class AsyncResource:
    """异步资源类

    通过实现 __aenter__ 和 __aexit__ 方法，使类成为异步上下文管理器
    这种方式适用于需要封装复杂状态管理的资源
    """

    def __init__(self, name):
        """初始化资源

        Args:
            name: 资源名称，用于标识不同的资源实例
        """
        self.name = name  # 资源名称
        self.is_open = False  # 资源状态标记

    async def __aenter__(self):
        """异步进入上下文管理器

        当执行 async with 语句时，会首先调用此方法
        负责资源的异步初始化和准备工作

        Returns:
            self: 返回资源实例，可在 async with 块中使用
        """
        print(f"打开资源: {self.name}")
        self.is_open = True  # 标记资源为已打开
        return self  # 返回资源实例供 async with 块使用

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文管理器

        当 async with 块执行完毕或发生异常时，会调用此方法
        负责资源的异步清理工作，无论块内是否发生异常都会执行

        Args:
            exc_type: 异常类型，如果没有异常则为 None
            exc_val: 异常值，如果没有异常则为 None
            exc_tb: 异常追踪对象，如果没有异常则为 None
        """
        print(f"关闭资源: {self.name}")
        self.is_open = False  # 标记资源为已关闭
        # 可以在这里处理异常，如果返回 True 则表示异常已被处理

    async def use(self):
        """使用资源的方法

        模拟实际使用资源的异步操作，检查资源状态并执行业务逻辑
        """
        if not self.is_open:
            raise RuntimeError("资源未打开")  # 状态检查
        print(f"使用资源: {self.name}")
        await asyncio.sleep(1)  # 模拟异步操作，不会阻塞事件循环


# 使用类实现的异步上下文管理器
async def use_resource():
    """使用异步资源

    演示如何使用通过类实现的异步上下文管理器
    async with 语法会自动处理资源的获取和释放
    """
    print("\n=== 演示类实现的异步上下文管理器 ===")
    # async with 会自动调用 __aenter__ 和 __aexit__
    async with AsyncResource("数据库连接") as resource:
        # 在块内可以安全使用资源
        await resource.use()
    # 块结束后，无论是否发生异常，都会自动调用 __aexit__ 关闭资源


# =============================================================================
# 方法2：使用装饰器实现异步上下文管理器
# 使用 @asynccontextmanager 装饰器可以更简洁地创建异步上下文管理器
# =============================================================================


@asynccontextmanager
async def managed_resource(name):
    """管理的资源上下文管理器

    使用 @asynccontextmanager 装饰器创建的异步上下文管理器
    yield 之前的代码相当于 __aenter__ 方法
    yield 之后的代码相当于 __aexit__ 方法
    yield 表达式的值会作为 async with as 变量的值

    Args:
        name: 资源名称

    Yields:
        name: 资源标识，传递给 async with 块使用
    """
    # 相当于 __aenter__ 方法：获取资源
    print(f"打开资源: {name}")
    try:
        # yield 表达式将控制权交给 async with 块
        # yield 的值会被绑定到 as 子句中的变量
        yield name
    finally:
        # 相当于 __aexit__ 方法：释放资源
        # 无论块内是否发生异常，finally 块都会执行
        print(f"关闭资源: {name}")


async def use_managed_resource():
    """使用管理的资源

    演示如何使用通过装饰器实现的异步上下文管理器
    """
    print("\n=== 演示装饰器实现的异步上下文管理器 ===")
    # async with 会执行装饰器函数中 yield 之前的代码
    async with managed_resource("文件连接") as resource:
        # resource 变量绑定到 yield 表达式的值
        print(f"使用资源: {resource}")
        await asyncio.sleep(1)  # 模拟异步操作
    # 块结束后，会执行 yield 之后的代码


# 主函数，按顺序执行所有示例
async def main():
    """主异步函数

    按顺序执行两个资源使用示例
    """
    print("开始执行异步上下文管理器示例...")
    # 执行第一个示例：类实现的异步上下文管理器
    await use_resource()
    # 执行第二个示例：装饰器实现的异步上下文管理器
    await use_managed_resource()
    print("\n所有异步上下文管理器示例执行完毕")


# 程序入口点
# 在 Python 中运行异步代码的标准方式
if __name__ == "__main__":
    # asyncio.run() 会创建事件循环，运行主异步函数，然后关闭事件循环
    asyncio.run(main())
