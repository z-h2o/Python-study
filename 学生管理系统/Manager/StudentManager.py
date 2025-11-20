from Student.student import Student
from Manager.Store import Store

class StudentManager(object):
    def __init__(self):
        self.students = Store().students
    
    # 显示菜单
    def show_menu(self):
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改学生信息")
        print("4. 显示所有学生")
        print("0. 退出系统")

    # 选择菜单选项
    def choose_menu(self):
        choice = input("请输入您的选择:")
        if choice == "1":
            self.add_student()
        elif choice == "2":
            self.del_student()
        elif choice == "3":
            self.update_student()
        elif choice == "4":
            self.show_all_students()
        elif choice == "0":
            self.save_students()
            print("谢谢使用，再见！")
            exit()
        else:
            print("您的选择有误，请重新输入")
    
    # 添加学生
    def add_student(self):
        name = input("请输入学生姓名:")
        age = input("请输入学生年龄:")
        sex = input("请输入学生性别:")
        s = Student(None, name, age, sex)
        self.students.append(s)
        print("添加学生成功")

    # 删除学生
    def del_student(self):
        id = input("请输入要删除的学生学号:")
        for student in self.students:
            if student.id == str(id):
                self.students.remove(student)
                print("删除学生成功")
                return
        else:
            print(f"删除学生失败, 学号为{id}的学生不存在")
    
    # 修改学生信息
    def update_student(self):
        id = input("请输入要修改的学生学号:")
        # 判断学号是否存在
        for student in self.students:
            if student.id == str(id):
                name = input("请输入学生姓名:")
                age = input("请输入学生年龄:")
                sex = input("请输入学生性别:")
                student.name = name
                student.age = age
                student.sex = sex
                print("修改学生信息成功")
                return
        else:
            print(f"修改学生信息失败, 学号为{id}的学生不存在")

    # 显示所有学生信息
    def show_all_students(self):
        if self.students:
            for student in self.students:
                print(student)
        else:
            print("当前系统中没有学生信息")

    # 保存学生信息
    def save_students(self):
        Store.write_student(self.students)