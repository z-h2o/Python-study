import os
from Student.student import Student

class Store(object):
    # 类变量：数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), "db.txt")

    def __init__(self):
        self.students = []
        self.init_students()

    # 静态方法：写入学生信息到数据库
    @staticmethod
    def write_student(students):
        with open(Store.db_path, 'w') as f:
            for student in students:
                f.write(f"{student.id},{student.name},{student.age},{student.sex}\n")

    # 初始化学生数据
    def init_students(self):
        with open(self.db_path, 'r') as f:
            for line in f.readlines(): 
                line = line.strip()
                id, name, age, sex = line.split(',')
                student = Student(id, name, age, sex)
                self.students.append(student)





