import time
from server import ChatServer
from client import ChatClient

def main():
    print('欢迎使用简易聊天室')
    
    while True:
        choice = input('请选择模式：1. 服务器模式 2. 客户端模式 0. 退出\n')
        if choice == '1':
            print('正在启动服务器...')
            time.sleep(1)
            server = ChatServer()
            server.start()
        elif choice == '2':
            nickname = input('请输入您的昵称：\n')
            print('正在连接服务器...')
            time.sleep(1)
            client = ChatClient()
            client.start(nickname)
        elif choice == '0':
            print('谢谢使用，再见！')
            break
        else:
            print('输入有误，请重新输入！')

if __name__ == '__main__':
    main()