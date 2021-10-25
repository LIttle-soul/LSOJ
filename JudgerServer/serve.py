import queue
import pymysql
import socket
from queue import Queue
import json
import time
import threading
import os
from file_serve import FileServer

# 判题服务


class JudgerServer:
    def __init__(self):
        self.queue = Queue()
        self.data_base = None
        self.mutex = threading.Lock()
        self.judger_json = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setDataBase(self):
        json_file = open("./config/server_setting.json")
        self.judger_json = json.loads(json_file.read())
        json_file.close()

        try:
            self.data_base = pymysql.connect(
                host=self.judger_json["db_ip"],
                user=self.judger_json["db_user"],
                port=int(self.judger_json["db_port"]),
                password=self.judger_json["db_password"],
                database=self.judger_json["db_database"],
                charset='utf8mb4'
            )
            print("数据库连接成功")
        except Exception as e:
            print(e)
            exit(1)

    def setServe(self):
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(
            ("0.0.0.0", self.judger_json["judger_server_port"]))
        self.server_socket.listen(20)
        print("server is running")

    def getSolution(self):
        cursor = self.data_base.cursor()
        while True:
            time.sleep(5)
            if self.queue.qsize() < 5 and self.mutex.acquire():
                cursor.execute(
                    'SELECT * FROM `solution` WHERE run_result<2 LIMIT 10;')
                data = cursor.fetchall()
                try:
                    for d in data:
                        # print(d)
                        self.queue.put(d[0])
                        cursor.execute(
                            f"UPDATE `solution` SET run_result = '2' WHERE solution_id = {d[0]}")
                    self.data_base.commit()
                except:
                    self.data_base.rollback()
                self.mutex.release()
        self.data_base.close()

    def deal_client(self, newSocket: socket, addr):
        print(newSocket, addr)
        status = False
        cursor = self.data_base.cursor()
        falsetime = 0
        while True:
            time.sleep(2)
            if self.mutex.acquire():
                try:
                    if status == True and self.queue.empty() is not True:
                        id = self.queue.get()
                        newSocket.send((f"judger|{id}").encode("utf-8"))
                        status = False
                    else:
                        newSocket.send("getStatus".encode("utf-8"))
                        data = newSocket.recv(1024)
                        recv_data = data.decode("utf-8")
                        if recv_data == "ok":
                            falsetime = 0
                            status = True
                        else:
                            falsetime = falsetime + 1
                            status = False
                            if falsetime >= 3600:
                                newSocket.send("timeOut".encode("utf-8"))
                                newSocket.close()
                                self.mutex.release()
                                return
                except socket.error:
                    newSocket.close()
                    self.mutex.release()
                    return
                except:
                    print("error")
                    self.mutex.release()
                    return
                self.mutex.release()

    def run(self):
        pass


if __name__ == "__main__":
    judger_server = JudgerServer()
    judger_server.setDataBase()
    judger_server.setServe()
    solution = threading.Thread(target=judger_server.getSolution)
    solution.setDaemon(True)
    solution.start()
    # file_serve = FileServer()
    # file_serve.run()
    while True:
        try:
            newSocket, addr = judger_server.server_socket.accept()
        except KeyboardInterrupt:
            judger_server.close()
            break
        print(f"client {addr} is connected!")
        client = threading.Thread(
            target=judger_server.deal_client, args=(newSocket, addr,))
        client.setDaemon(True)
        client.start()
