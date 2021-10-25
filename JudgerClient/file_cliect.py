import socket
import tarfile
import tqdm
import os
import json


class FileClient:
    def __init__(self) -> None:
        jsonfile = open("./config/client_setting.json", 'r')
        judger_json = json.loads(jsonfile.read())
        jsonfile.close()
        self.server_host = judger_json["server_host"] or "127.0.0.1"
        self.server_port = judger_json["file_server_port"] or 8087
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.udp_socket.connect((self.server_host, self.server_port))

        self.buffer_size = 1024*50

        self.problem_data_path = judger_json['problem_data_path'] or './ProblemData/'
        self.problem_targz_path = judger_json['problem_targz_path'] or './ProblemZipData/'

        if not os.path.exists(self.problem_data_path):
            os.makedirs(self.problem_data_path)

        if not os.path.exists(self.problem_targz_path):
            os.makedirs(self.problem_targz_path)

    def untar(self, problem_id='all_data'):
        try:
            t = tarfile.open(
                f"{self.problem_targz_path}{problem_id}.tar.gz")
            if problem_id == 'all_data':
                t.extractall(path=f"{self.problem_data_path}")
            else:
                t.extractall(path=f"{self.problem_data_path}{problem_id}")
            return True
        except Exception as e:
            print(e)
            return False

    def get_create_time(self, problem_id='all_data'):
        return os.stat(path=f"{self.problem_targz_path}{problem_id}.tar.gz").st_ctime

    def get_file_size(self, problem_id='all_data'):
        return os.stat(path=f"{self.problem_targz_path}{problem_id}.tar.gz.torren").st_size

    def get_file(self, problem_id='all_data', agreement='tcp', pointbreak=0):
        if agreement == 'tcp':
            self.tcp_socket.send(f"get_file_size {problem_id}".encode('utf-8'))
            file_size = int(self.tcp_socket.recv(1024).decode('utf-8'))
            if file_size == 0:
                return False
            # print(file_size)
            progress = tqdm.tqdm(
                total=file_size,
                desc=f"接受文件{problem_id}",
                unit='B',
                unit_divisor=1024,
                unit_scale=True,
                colour='green'
            )
            if pointbreak > 0:
                cur_point = pointbreak
                progress.update(cur_point)
                with open(f"{self.problem_targz_path}{problem_id}.tar.gz.torren", "ab") as f:
                    self.tcp_socket.send(
                        f"get_file_by_pointbreak {problem_id} {pointbreak}".encode('utf-8'))
                    while True:
                        bytes_read = self.tcp_socket.recv(self.buffer_size)
                        if bytes_read == b'file_eof':
                            print('传输完成')
                            break
                        f.write(bytes_read)
                        progress.update(len(bytes_read))
            else:
                with open(f"{self.problem_targz_path}{problem_id}.tar.gz.torren", "wb") as f:
                    self.tcp_socket.send(
                        f"get_file {problem_id}".encode('utf-8'))
                    while True:
                        bytes_read = self.tcp_socket.recv(self.buffer_size)
                        if bytes_read == b'file_eof':
                            print('传输完成')
                            break
                        f.write(bytes_read)
                        progress.update(len(bytes_read))
            self.tcp_socket.send('exit'.encode('utf-8'))
            self.tcp_socket.close()
            if os.path.exists(f"{self.problem_targz_path}{problem_id}.tar.gz"):
                os.remove(f"{self.problem_targz_path}{problem_id}.tar.gz")
            os.rename(f"{self.problem_targz_path}{problem_id}.tar.gz.torren",
                      f"{self.problem_targz_path}{problem_id}.tar.gz")
            self.untar(problem_id=problem_id)
            return True

        elif agreement == 'udp':
            address = (self.server_host, self.server_port)
            self.udp_socket.sendto(
                f"get_file_size {problem_id}".encode('utf-8'), address)
            message, address = self.udp_socket.recvfrom(1024)
            file_size = int(message.decode('utf-8'))
            if file_size == 0:
                return False
            progress = tqdm.tqdm(
                total=file_size,
                desc=f"接受文件{problem_id}",
                unit='B',
                unit_divisor=1024,
                unit_scale=True,
                colour='green'
            )
            if pointbreak > 0:
                cur_point = pointbreak
                progress.update(cur_point)
                with open(f"{self.problem_targz_path}{problem_id}.tar.gz.torren", "ab") as f:
                    self.udp_socket.sendto(
                        f"get_file_by_pointbreak {problem_id} {pointbreak}".encode('utf-8'), address)
                    while True:
                        bytes_read, address = self.udp_socket.recvfrom(
                            self.buffer_size)
                        if bytes_read == b'file_eof':
                            print('传输完成')
                            break
                        f.write(bytes_read)
                        progress.update(len(bytes_read))
            else:
                with open(f"{self.problem_targz_path}{problem_id}.tar.gz.torren", "wb") as f:
                    self.udp_socket.sendto(
                        f"get_file {problem_id}".encode('utf-8'), address)
                    while True:
                        bytes_read, address = self.udp_socket.recvfrom(
                            self.buffer_size)
                        if bytes_read == b'file_eof':
                            print('传输完成')
                            break
                        f.write(bytes_read)
                        progress.update(len(bytes_read))
            self.udp_socket.sendto('exit'.encode('utf-8'), address)
            self.udp_socket.close()
            if os.path.exists(f"{self.problem_targz_path}{problem_id}.tar.gz"):
                os.remove(f"{self.problem_targz_path}{problem_id}.tar.gz")
            os.rename(f"{self.problem_targz_path}{problem_id}.tar.gz.torren",
                      f"{self.problem_targz_path}{problem_id}.tar.gz")
            self.untar(problem_id=problem_id)
            return True
        else:
            return False

    def handle_tcp_file(self, problem_id='all_data'):
        self.tcp_socket.connect((self.server_host, self.server_port))
        print(self.tcp_socket.recv(1024).decode('utf-8'))
        if os.path.exists(path=f"{self.problem_targz_path}{problem_id}.tar.gz"):
            self.tcp_socket.send(
                f"get_file_create_time {problem_id}".encode('utf-8'))
            serve_file_create_time = self.tcp_socket.recv(1024).decode('utf-8')
            client_file_create_time = str(
                self.get_create_time(problem_id=problem_id))
            # print(serve_file_create_time, client_file_create_time)
            if int(serve_file_create_time[:10]) <= int(client_file_create_time[:10]):
                self.tcp_socket.send('exit'.encode('utf-8'))
                self.tcp_socket.close()
                return True
            else:
                return self.get_file(problem_id=problem_id)
        else:
            if os.path.exists(path=f"{self.problem_targz_path}{problem_id}.tar.gz.torren"):
                file_size = self.get_file_size(problem_id=problem_id)
                return self.get_file(problem_id=problem_id, pointbreak=file_size)
            else:
                return self.get_file(problem_id=problem_id)

    def handle_udp_file(self, problem_id='all_data'):
        address = (self.server_host, self.server_port)
        if os.path.exists(path=f"{self.problem_targz_path}{problem_id}.tar.gz"):
            self.udp_socket.sendto(
                f"get_file_create_time {problem_id}".encode('utf-8'), address)
            serve_file_create_time, address = self.udp_socket.recvfrom(1024)
            serve_file_create_time = serve_file_create_time.decode('utf-8')
            if int(serve_file_create_time) == 0:
                return False
            client_file_create_time = str(
                self.get_create_time(problem_id=problem_id))
            # print(serve_file_create_time, client_file_create_time)
            if int(serve_file_create_time[:10]) <= int(client_file_create_time[:10]):
                self.udp_socket.sendto('exit'.encode('utf-8'), address)
                self.udp_socket.close()
                return True
            else:
                return self.get_file(problem_id=problem_id, agreement='udp')
        else:
            if os.path.exists(path=f"{self.problem_targz_path}{problem_id}.tar.gz.torren"):
                file_size = self.get_file_size(problem_id=problem_id)
                return self.get_file(problem_id=problem_id, agreement='udp', pointbreak=file_size)
            else:
                return self.get_file(problem_id=problem_id, agreement='udp')


if __name__ == "__main__":
    client = FileClient()
    client.handle_udp_file()
