from Manager.StudentManager import StudentManager

def main():
    print("欢迎使用学生管理系统")
    # 初始化学生数据
    manager = StudentManager()
    manager.show_menu()
    while True:
      manager.choose_menu()

if __name__ == "__main__":
    main()