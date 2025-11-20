import socket
import threading
import time

class ChatServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 55557
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message, sender=None):
        # 创建列表副本以避免遍历过程中被修改
        for client in self.clients:
            if client != sender:
                client.send(message)
    
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    # 客户端主动关闭连接
                    break
                self.broadcast(message, client)
            except:
                # 其他异常情况
                break
        # 执行退出逻辑
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        nickname = self.nicknames[index]
        self.nicknames.remove(nickname)
        self.broadcast(f'{nickname} 退出了聊天室！'.encode('utf-8'))
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f'服务器已启动，正在监听 {self.host}:{self.port}')
        
        while True:
            client, address = server.accept()
            print(f'连接成功：{str(address)}')
            
            # 请求并存储昵称
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f'用户昵称：{nickname}')
            self.broadcast(f'{nickname} 加入了聊天室！'.encode('utf-8'))
            client.send('成功连接到服务器！'.encode('utf-8'))
            
            # 为客户端创建线程
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == '__main__':
    server = ChatServer()
    server.start()