import socket
import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.serve = Socket(port)
        self.client = {}

    def run(self):
        print ("开始线程：" + self.name + str(self.counter))
        while True:
            self.client[addr[0]], addr = self.serve.server_socket.accept()
            print(addr)
            if self.counter == 1:
                self.serve.send_message(self.client[addr[0]], b"Hello, thread 1")
            elif self.counter == 2:
                self.serve.get_message(self.client[addr[0]])
        print ("退出线程：" + self.name)
    
    def send(self, cliect, text):
        self.serve.send_message(cliect, text)

class Socket:
    def __init__(self, port):
        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.host = '0.0.0.0'
        self.port = port
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
    def send_message(self, client, text=b"Hello, User"):
        print("send线程")
        client.send(text)

    def get_message(self, client):
        print("get线程")
        try:
            while True:
                msg = client.recv(1024)
                text = msg.decode('utf-8')
                if text == 'q':
                    client.send("感谢你的本次使用，再见".encode())
                    client.close()
                    break
                print(text)
                thread1.send(client, b'Hello,' + msg)
        except:
            client.close()

    def close(self):
        self.server_socket.close()

if __name__=="__main__":
    thread1 = myThread(1, "Thread-1", 1, 8085)
    thread2 = myThread(1, "Thread-1", 2, 8086)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("退出")

        