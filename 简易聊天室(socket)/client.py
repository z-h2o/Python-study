import socket
import threading
import time

class ChatClient:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 55557
        
    def receive_message(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                print(message)
            except:
                print('连接已关闭！')
                break
    
    def start(self, nickname):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        
        # 处理服务器消息的线程
        receive_thread = threading.Thread(target=self.receive_message, args=(client,))
        receive_thread.start()
        
        # 发送昵称
        client.send(nickname.encode('utf-8'))
        
        # 发送消息
        while True:
            message = input('')
            if message == 'quit':
                client.close()
                break
            client.send(f'{nickname}: {message}'.encode('utf-8'))

if __name__ == '__main__':
    nickname = input('请输入您的昵称：')
    client = ChatClient()
    client.start(nickname)