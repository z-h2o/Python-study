# 导入所需模块：socket用于网络通信，threading用于多线程处理
import socket
import threading

# 聊天客户端类，实现TCP协议的聊天室客户端功能
class ChatClient:
    def __init__(self):
        # 服务器IP地址和端口号，需与服务器保持一致
        self.host = '127.0.0.1'
        self.port = 55557
    
    def receive_message(self, client):
        """
        接收服务器消息的方法
        :param client: 与服务器连接的socket对象
        """
        while True:
            try:
                # 接收服务器发送的消息（最多1024字节）并解码
                message = client.recv(1024).decode('utf-8')
                # 打印接收到的消息
                print(message)
            except:
                # 出现异常时（如服务器关闭）打印提示并退出循环
                print('连接已关闭！')
                break
    
    def start(self, nickname):
        """
        启动客户端的主方法
        :param nickname: 用户输入的昵称
        """
        # 创建TCP socket对象
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到服务器
        client.connect((self.host, self.port))
        
        # 创建独立线程处理服务器消息（避免阻塞主线程）
        receive_thread = threading.Thread(target=self.receive_message, args=(client,))
        receive_thread.start()
        
        # 发送用户昵称给服务器
        client.send(nickname.encode('utf-8'))
        
        # 持续接收用户输入并发送消息
        while True:
            message = input('')  # 等待用户输入消息
            if message == 'quit':  # 如果用户输入quit，则退出聊天
                client.close()  # 关闭与服务器的连接
                break
            # 格式化消息（包含昵称）并发送给服务器
            client.send(f'{nickname}: {message}'.encode('utf-8'))

# 主程序入口
if __name__ == '__main__':
    # 提示用户输入昵称
    nickname = input('请输入您的昵称：')
    # 创建客户端实例
    client = ChatClient()
    # 启动客户端
    client.start(nickname)