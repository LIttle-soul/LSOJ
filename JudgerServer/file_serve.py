import socket
import tqdm
import os
from time import sleep, time
import threading
import tarfile
import json


class FileServer:
    def __init__(self) -> None:
        json_file = open("./config/server_setting.json")
        self.judger_json = json.loads(json_file.read())
        json_file.close()
        self.host = "0.0.0.0"
        self.port = self.judger_json['file_server_port'] or 8807
        self.mutex = threading.Lock()
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_socket.bind((self.host, self.port))
        self.udp_socket.bind((self.host, self.port))
        self.tcp_socket.listen(5)
        # 文件缓冲区
        self.buffer_size = 1024*50
        # 问题数据存放地址
        self.problem_data_path = self.judger_json['problem_data_path'] or "./ProblemData/"
        self.problem_targz_path = self.judger_json['problem_targz_path'] or "./ProblemZipFile/"
        # 帮助内容
        self.help_text = """
帮助文档

    get_file_size <problem_id[String | 'all_data']>: 获取文件大小
    get_file_create_time <problem_id[String | 'all_data']>: 获取文件创建时间
    get_file <problem_id[String | 'all_data']>: 获取文件
    get_file_by_pointbreak <problem_id[String | 'all_data']> <pointbreak[String | '0']>: 从短点处获取文件
    update_file <problem_id[String | 'all_data']>: 更新压缩文件
    help: 获取帮助信息
    exit: 退出服务
"""
        # 文件夹创建
        if not os.path.exists(self.problem_targz_path):
            os.makedirs(self.problem_targz_path)

    # TCP 协议获取文件
    def get_tcp_client(self):
        print("TCP服务端启动成功\n")
        target = {}
        while True:
            try:
                client, address = self.tcp_socket.accept()
                print(
                    f"客户端: (IP: {address[0]}\tPort: {address[1]})\n连接协议: TCP\n")
                message = """
欢迎访问 TCP 题库文件服务，请传入要执行的操作:
    get_file_size <problem_id[String | 'all_data']>: 获取文件大小
    get_file_create_time <problem_id[String | 'all_data']>: 获取文件创建时间
    get_file <problem_id[String | 'all_data']>: 获取文件
    get_file_by_pointbreak <problem_id[String | 'all_data']> <pointbreak[String | '0']>: 从短点处获取文件
    update_file <problem_id[String | 'all_data']>: 更新压缩文件
    help: 获取帮助信息
    exit: 退出服务
"""
                client.send(message.encode('utf-8'))
                target = threading.Thread(
                    target=self.handle_tcp_client, args=(client,), name=address[0])
                target.setDaemon(daemonic=True)
                target.start()
            except ConnectionResetError:
                client.close()
                continue
            except KeyboardInterrupt:
                self.tcp_socket.close()
                break

    def handle_tcp_client(self, client=None):
        try:
            while True:
                message = client.recv(1024).decode('utf-8').split()
                # print(message)
                if message[0] == 'get_file_size':
                    data = self.get_file_size(problem_id=message[1])
                    client.send(str(data).encode('utf-8'))
                elif message[0] == 'get_file_create_time':
                    data = self.get_create_time(problem_id=message[1])
                    client.send(str(data).encode('utf-8'))
                elif message[0] == 'get_file':
                    self.send_file(problem_id=message[1], client=client)
                elif message[0] == 'get_file_by_pointbreak':
                    self.send_file(
                        problem_id=message[1], client=client, pointbreak=int(message[2]))
                elif message[0] == 'update_file':
                    self.make_targz(problem_id=message[1])
                elif message[0] == 'help':
                    client.send(self.help_text.encode('utf-8'))
                elif message[0] == 'exit':
                    client.close()
                    break
        except ConnectionResetError:
            client.close()
            return
        except KeyboardInterrupt:
            client.close()
            return

    def get_udp_client(self):
        print("UDP服务端启动成功\n")
        while True:
            try:
                message, address = self.udp_socket.recvfrom(self.buffer_size)
                message = message.decode('utf-8').split()
                print(message)
                if message[0] == 'get_file_size':
                    data = self.get_file_size(problem_id=message[1])
                    self.udp_socket.sendto(str(data).encode('utf-8'), address)
                elif message[0] == 'get_file_create_time':
                    data = self.get_create_time(problem_id=message[1])
                    self.udp_socket.sendto(str(data).encode('utf-8'), address)
                elif message[0] == 'get_file':
                    get_file_thread = threading.Thread(target=self.send_file(
                        problem_id=message[1], client=address, agreement='udp'))
                    get_file_thread.setDaemon(True)
                    get_file_thread.start()
                elif message[0] == 'get_file_by_pointbreak':
                    get_file_thread = threading.Thread(target=self.send_file(
                        problem_id=message[1], client=address, agreement='udp', pointbreak=int(message[2])))
                    get_file_thread.setDaemon(True)
                    get_file_thread.start()
                elif message[0] == 'update_file':
                    self.make_targz(problem_id=message[1])
                elif message[0] == 'help':
                    self.udp_socket.sendto(
                        self.help_text.encode('utf-8'), address)
                elif message[0] == 'exit':
                    self.udp_socket.sendto(f"欢迎下次使用".encode('utf-8'), address)
            except ConnectionResetError:
                continue
            except KeyboardInterrupt:
                self.udp_socket.close()
                return

    def make_targz(self, problem_id='all_data'):
        try:
            if problem_id != 'all_data' and not os.path.exists(path=f"{self.problem_data_path}{problem_id}"):
                return False
            if self.mutex.acquire():
                with tarfile.open(f"{self.problem_targz_path}{problem_id}.tar.gz", "w:gz") as tar:
                    if problem_id == 'all_data':
                        tar.add(
                            name=f"{self.problem_data_path[:-1]}", arcname="/")
                    else:
                        tar.add(name=f"{self.problem_data_path}{problem_id}",
                                arcname="/")
                self.mutex.release()
            else:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def get_create_time(self, problem_id='all_data'):
        if not os.path.exists(path=f"{self.problem_targz_path}{problem_id}.tar.gz"):
            if self.make_targz(problem_id=problem_id):
                return os.stat(path=f"{self.problem_targz_path}{problem_id}.tar.gz").st_ctime
            else:
                return 0
        else:
            return os.stat(path=f"{self.problem_targz_path}{problem_id}.tar.gz").st_ctime

    def get_file_size(self, problem_id='all_data'):
        if not os.path.exists(path=f"{self.problem_targz_path}{problem_id}.tar.gz"):
            if self.make_targz(problem_id=problem_id):
                return os.stat(path=f"{self.problem_targz_path}{problem_id}.tar.gz").st_size
            else:
                return 0
        else:
            return os.stat(path=f"{self.problem_targz_path}{problem_id}.tar.gz").st_size

    def send_file(self, problem_id='all_data', client=None, agreement='tcp', pointbreak=0):
        file_path = f"{self.problem_targz_path}{problem_id}.tar.gz"

        if not os.path.exists(file_path):
            self.make_targz(problem_id=problem_id)

        file_size = self.get_file_size(problem_id=problem_id)

        progress = tqdm.tqdm(
            total=file_size,
            desc=f'发送文件{file_path}',
            unit='B',
            unit_divisor=1024,
            unit_scale=True,
            colour='green'
        )
        cur_point = pointbreak
        progress.update(cur_point)
        if agreement == 'tcp':
            with open(file_path, "rb") as f:
                if cur_point > 0:
                    f.seek(cur_point)
                while cur_point < file_size:
                    bytes_read = f.read(self.buffer_size)
                    client.sendall(bytes_read)
                    cur_point += len(bytes_read)
                    progress.update(len(bytes_read))
                    sleep(0.001)
                print('文件传输完毕！')
                client.sendall('file_eof'.encode('utf-8'))
        else:
            with open(file_path, "rb") as f:
                if cur_point > 0:
                    f.seek(cur_point)
                while cur_point < file_size:
                    bytes_read = f.read(self.buffer_size)
                    self.udp_socket.sendto(bytes_read, client)
                    progress.update(len(bytes_read))
                    cur_point += len(bytes_read)
                    sleep(0.001)
                print('文件传输完毕！')
                self.udp_socket.sendto(
                    'file_eof'.encode('utf-8'), client)

    def run(self):
        tcp_server = threading.Thread(target=self.get_tcp_client)
        udp_server = threading.Thread(target=self.get_udp_client)
        tcp_server.setDaemon(daemonic=True)
        udp_server.setDaemon(daemonic=True)
        tcp_server.start()
        udp_server.start()
        tcp_server.join()
        udp_server.join()


if __name__ == "__main__":
    serve = FileServer()
    serve.run()
