from typing import Any, Callable


class Validator(object):
    """数据验证器"""

    def __init__(self):
        self.rules: list[Callable] = []

    def add_rule(self, rule: Callable) -> "Validator":
        """添加验证规则"""
        self.rules.append(rule)
        return self

    def validate(self, data: Any) -> dict[str, Any]:
        """验证数据"""
        errors = []
        for rule in self.rules:
            try:
                rule(data)
            except Exception as e:
                errors.append(e)
        return {"valid": len(errors) == 0, "errors": errors}


# 验证是否是字符串
def is_string(value: Any) -> bool:
    """验证是否是字符串"""
    if not isinstance(value, str):
        raise ValueError("不是字符串")


def is_not_empty(value: Any) -> bool:
    """验证是否不为空"""
    if value is None or value == "":
        raise ValueError("不能为空")


# 验证长度是否在指定范围内
def is_length_in_range(min_len: int, max_len: int) -> bool:
    """验证长度是否在指定范围内"""

    def lengthValid(value):
        if len(value) < min_len or len(value) > max_len:
            raise ValueError(f"长度必须在 {min_len} 到 {max_len} 之间")

    return lengthValid


def print_args():
    def arges(data):
        print(f"传入的参数为: {data}")

    return arges


v = (
    Validator()
    .add_rule(print_args())
    .add_rule(is_string)
    .add_rule(is_not_empty)
    .add_rule(is_length_in_range(1, 5))
)

res1 = v.validate(9)
print("res=>1", res1)

res2 = v.validate("测试的字🔢1")
print("res==>2", res2)


# 递归取出斐波那契数列的前n项
def fibonacci(n):
    def fib(m):
        """递归取出斐波那契数列的前n项"""
        if m < 2:
            return m
        else:
            return fib(m - 1) + fib(m - 2)

    v = fib(n)
    return v


print(fibonacci(5))


def fib1(n: int) -> int:
    if n < 2:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


print(fib1(5), fib1(9), fib1(10), fib1(11))
