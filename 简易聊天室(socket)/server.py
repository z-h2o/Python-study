# 导入所需模块：socket用于网络通信，threading用于多线程处理
import socket
import threading

# 聊天服务器类，实现TCP协议的多人聊天室功能
class ChatServer:
    # 初始化服务器配置
    def __init__(self):
        self.host = '127.0.0.1'  # 服务器IP地址（本地回环地址）
        self.port = 55557  # 服务器端口号
        self.clients = []  # 存储所有连接的客户端socket对象
        self.nicknames = []  # 存储对应客户端的用户昵称
        
    # 广播消息给所有客户端（可选排除发送者）
    def broadcast(self, message, sender=None):
        # 遍历所有客户端
        for client in self.clients:
            if client != sender:  # 不将消息发送回原发送者
                client.send(message)
    
    # 处理单个客户端的消息循环
    def handle_client(self, client):
        while True:
            try:
                # 接收客户端消息（最多1024字节）
                message = client.recv(1024)
                if not message:  # 如果客户端主动关闭连接
                    break
                # 给发送消息的用户单独回复"正在监听中..."
                client.send('正在监听中...'.encode('utf-8'))
                self.broadcast(message, client)  # 广播收到的消息
            except Exception:
                # 处理其他异常情况（如网络错误）
                break
        # 执行客户端退出逻辑
        index = self.clients.index(client)  # 获取客户端在列表中的索引
        self.clients.remove(client)  # 从客户端列表移除
        client.close()  # 关闭socket连接
        nickname = self.nicknames[index]  # 获取对应的用户昵称
        self.nicknames.remove(nickname)  # 从昵称列表移除
        # 广播用户退出通知
        self.broadcast(f'{nickname} 退出了聊天室！'.encode('utf-8'))
    
    # 启动服务器主函数
    def start(self):
        # 创建TCP socket对象
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))  # 绑定IP和端口
        server.listen()  # 开始监听连接请求
        print(f'服务器已启动，正在监听 {self.host}:{self.port}')
        
        # 持续接受客户端连接
        while True:
            client, address = server.accept()  # 接受客户端连接
            
            
            # 请求并存储客户端昵称
            nickname = client.recv(1024).decode('utf-8')  # 接收并解码昵称
            self.nicknames.append(nickname)  # 保存昵称
            self.clients.append(client)  # 保存客户端socket

            print(f'用户昵称：{nickname}---->连接成功：{str(address)}')

            # 广播新用户加入通知
            self.broadcast(f'{nickname} 加入了聊天室！'.encode('utf-8'))
            # client.send('成功连接到服务器！'.encode('utf-8'))  # 向新客户端发送连接成功消息
            
            # 为客户端创建独立线程处理消息
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()  # 启动线程

# 主程序入口
if __name__ == '__main__':
    server = ChatServer()  # 创建服务器实例
    server.start()  # 启动服务器