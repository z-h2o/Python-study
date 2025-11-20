import random

class Student(object):
    def __init__(self, id, name, age, sex):
        self.id = id or random.randint(1000, 9999)
        self.name = name or "未知"
        self.age = age or "未知"
        self.sex = sex or "未知"
        
    def __str__(self):
        return f"学号：{self.id}，姓名：{self.name}，年龄：{self.age}，性别：{self.sex}"