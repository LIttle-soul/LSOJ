from shutil import ExecError
from subprocess import call
import pymysql.cursors
import socket
import json
import time
import threading
from util import _judger
import os
import time
import datetime
import logging
# import requests


class GlobalVar:
    def __init__(self):
        self.status = True
        self.data_time_json = {}
        self.judger_json = {}
        self.judger_name = "LSOJ_Judger"
        self.host = "127.0.0.1"
        self.port = 22
        self.python2_path = "/usr/bin/python2"
        self.python3_path = "/usr/bin/python3"
        self.data_base = None
        self.cursor = None
        self.client_socket = None
        self.logger = None

    def setLogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("judger.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

        self.logger.info("Start print log")

    def setGlobalVar(self):
        self.setLogger()
        self.status = True

        myjsonfile = open("./config/setting.json", 'r')
        self.judger_json = json.loads(myjsonfile.read())
        myjsonfile.close()

        datajsonfile = open("./config/datatime.json", 'r')
        self.data_time_json = json.loads(datajsonfile.read())
        datajsonfile.close()

        self.judger_name = socket.gethostbyname(socket.gethostname())
        self.logger.info("Judger name: " + self.judger_name)

        self.host = self.judger_json["server_ip"]
        self.port = self.judger_json["server_port"]
        self.python3_path = self.judger_json["python3_path"]
        self.python2_path = self.judger_json["python2_path"]

        self.logger.info("Connecting database !")
        self.data_base = pymysql.connect(
            host=self.judger_json["db_ip"],
            user=self.judger_json["db_user"],
            port=int(self.judger_json["db_port"]),
            password=self.judger_json["db_password"],
            database=self.judger_json["db_database"],
            charset='utf8mb4'
        )
        self.cursor = self.data_base.cursor()
        self.logger.info("Connect db succeed!")

        self.logger.info("Connecting judger server!")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.logger.info("Connect judger server succeed!")

    def reconnect(self):
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.data_base = pymysql.connect(
                host=self.judger_json["db_ip"],
                user=self.judger_json["db_user"],
                port=int(self.judger_json["db_port"]),
                password=self.judger_json["db_password"],
                database=self.judger_json["db_database"],
                charset='utf8mb4'
            )
            self.cursor = self.data_base.cursor()
            # self.client_socket.connect((self.host, self.port))
            self.status = True
        except Exception as e:
            self.logger.error("Connect db failed!")
            self.logger.error(repr(e))
            pass


class Solution:
    def __init__(self):
        self.judger_name = global_var.judger_name
        self.data_base = global_var.data_base
        self.cursor = global_var.cursor

    def getSolutionData(self, id):
        sql = f"""SELECT
	                solution.solution_id, 
	                solution.problem_id, 
	                solution.user_id, 
	                solution.contest_id, 
	                solution.solution_code, 
	                solution.solution_language, 
	                solution.solution_time, 
	                solution.code_length, 
	                problem.problem_spj, 
	                problem.time_limit, 
	                problem.memory_limit
                FROM
	                solution
	            INNER JOIN
	                problem
	            ON 
		            solution.problem_id = problem.problem_id
                WHERE
	                solution_id = {id};"""
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # print(data)
        return data

    def compileError(self, id, message):
        sql = f"""UPDATE
	                solution
                SET
	                run_result = '11',
	                run_error = '{message}'
                WHERE
	                solution_id = {id};"""
        self.cursor.execute(sql)
        self.data_base.commit()

    def doneProblem(self, id, code_length, run_time, run_memory, run_result, run_error, run_pass_rate, run_all_rate):
        sql = f"""UPDATE
                    solution 
                SET 
                    code_length = '{code_length}',
                    run_time = '{run_time}',
                    run_memory = '{run_memory}',
                    run_result = '{run_result}',
                    run_error = '{run_error}',
                    run_pass_rate = '{run_pass_rate}',
                    run_all_rate = '{run_all_rate}'
                WHERE
	                solution_id = {id};"""
        self.cursor.execute(sql)
        self.data_base.commit()


class Judger:
    def __init__(self):
        self.judger_name = global_var.judger_name
        self.outputpath = global_var.judger_name + "temp.out"
        self.errorpath = global_var.judger_name + "error.out"

    def run(self, language, timelimit, memorylimit, inputpath):
        if language == 0:
            return self.judgeC(timelimit, memorylimit, inputpath)
        elif language == 1:
            return self.judgeCPP(timelimit, memorylimit, inputpath)
        elif language == 3:
            return self.judgePython2(timelimit, memorylimit, inputpath)
        elif language == 4:
            return self.judgePython3(timelimit, memorylimit, inputpath)
        else:
            # 写入数据库语言选择错误
            global_var.status = True
            return False

    def judgeC(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=self.judger_name+".o",
                           input_path=inputpath,
                           output_path=self.outputpath,
                           error_path=self.errorpath,
                           args=[],
                           # can be empty list
                           env=[],
                           log_path=self.judger_name+"judger.log",
                           # can be None
                           seccomp_rule_name="c_cpp",
                           uid=0,
                           gid=0
                           )

    def judgeCPP(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=self.judger_name+".o",
                           input_path=inputpath,
                           output_path=self.outputpath,
                           error_path=self.errorpath,
                           args=[],
                           # can be empty list
                           env=[],
                           log_path=self.judger_name+"judger.log",
                           # can be None
                           seccomp_rule_name="c_cpp",
                           uid=0,
                           gid=0
                           )

    def judgePython2(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=global_var.python2_path,
                           input_path=inputpath,
                           output_path=self.outputpath,
                           error_path=self.errorpath,
                           args=[f"{self.judger_name}.py"],
                           # can be empty list
                           env=[],
                           log_path=self.judger_name+"judger.log",
                           # can be None
                           seccomp_rule_name="general",
                           uid=0,
                           gid=0
                           )

    def judgePython3(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=global_var.python3_path,
                           input_path=inputpath,
                           output_path=self.outputpath,
                           error_path=self.errorpath,
                           args=[f"{self.judger_name}.py"],
                           # can be empty list
                           env=[],
                           log_path=self.judger_name+"judger.log",
                           # can be None
                           seccomp_rule_name="general",
                           uid=0,
                           gid=0
                           )


class Compile:
    def __init__(self):
        self.judger_name = global_var.judger_name
        self.solution = Solution()

    def run(self, id, problem, language, code):
        language = int(language)
        # print(
        #     f"id: {id}\t problem: {problem}\t language: {language}\n code:\n {code}\n")
        if language == 0:
            return self.compileC(id, problem, code)
        elif language == 1:
            return self.compileCPP(id, problem, code)
        elif language == 3 or language == 4:
            return self.compilePython(id, problem, code)
        else:
            # 写入数据库语言选择错误
            # print("语言选择错误")
            global_var.status = True
            return False

    def checkSensitiveWord(self, word):
        if os.environ.get("PYTHONSWF") != "yes":
            return "0"
        elif word.find("thread") >= 0:
            return "thread"
        elif word.find("process") >= 0:
            return "process"
        elif word.find("resource") >= 0:
            return "resource"
        elif word.find("ctypes") >= 0:
            return "ctypes"
        elif word.find(" os") >= 0:
            return " os"
        elif word.find("__import__") >= 0:
            return "__import__"
        elif word.find("eval") >= 0:
            return "eval"
        elif word.find("exec") >= 0:
            return "exec"
        elif word.find("globals") >= 0:
            return "globals"
        elif word.find("locals") >= 0:
            return "locals"
        elif word.find("compile") >= 0:
            return "compile"
        elif word.find("frame") >= 0:
            return "frame"
        else:
            return "0"

    # C语言编译
    def compileC(self, id, problem, code):
        file = open(f'{self.judger_name}.c', 'w', encoding='utf-8')
        file.write(code)
        file.close()
        cmd = f'timeout 10 gcc {self.judger_name}.c -fmax-errors=3 -o {self.judger_name}.o -O2 -std=c11 2>{self.judger_name}ce.txt'
        result = os.system(cmd)
        if result:
            try:
                filece = open(f"{self.judger_name}ce.txt", "r")
                msg = str(filece.read())
                if msg == "":
                    msg = "Compile timeout! Maybe you define too big arrays!"
                filece.close()
                # 写入数据库，编译错误以及错误信息
                self.solution.compileError(id=id, message=msg)
                global_var.status = True
            except:
                msg = "Fatal Compile error!"
                # 写入数据库，编译错误以及错误信息
                self.solution.compileError(id=id, message=msg)
                global_var.status = True
            # print(id, code, self.judger_name, problem)
            return False
        # print(id, code, self.judger_name, problem)
        return True

    def compileCPP(self, id, problem, code):
        file = open(f'{self.judger_name}.cpp', 'w', encoding='utf-8')
        file.write(code)
        file.close()
        cmd = f'timeout 10 g++ {self.judger_name}.cpp -fmax-errors=3 -o {self.judger_name}.o -O2 -std=c++14 2>{self.judger_name}ce.txt'
        result = os.system(cmd)
        if result:
            try:
                filece = open(f"{self.judger_name}ce.txt", "r")
                msg = str(filece.read())
                if msg == "":
                    msg = "Compile timeout! Maybe you define too big arrays!"
                filece.close()
                # 写入数据库，编译错误以及错误信息
                self.solution.compileError(id=id, message=msg)
                global_var.status = True
            except:
                msg = "Fatal Compile error!"
                # 写入数据库，编译错误以及错误信息
                self.solution.compileError(id=id, message=msg)
                global_var.status = True
            # print(id, code, self.judger_name, problem)
            return False
        # print(id, code, self.judger_name, problem)
        return True

    def compilePython(self, id, problem, code):
        wo = self.checkSensitiveWord(code)
        if wo != "0":
            self.solution.compileError(
                id=id, message="Your code has sensitive words "+wo)
            global_var.status = True
            return False
        file = open(f"{self.judger_name}.py", "w", encoding='utf-8')
        # file.write("import sys\nblacklist = ['importlib','traceback','os']\nfor mod in blacklist:\n    i = __import__(mod)\n    sys.modules[mod] = None\ndel __builtins__.__dict__['eval']\ndel __builtins__.__dict__['locals']\ndel __builtins__.__dict__['open']\n" +code)
        file.write(code)
        file.close()
        return True


class JudgerRun:
    def __init__(self):
        self.outputpath = global_var.judger_name + "temp.out"
        self.errorpath = global_var.judger_name + "error.out"

        self.max_memory = 0
        self.max_time = 0

        self.my_result = 100
        self.test_case = ""
        self.my_time = 0
        self.my_memory = 0

        self.run_pass_rate = 0
        self.run_all_rate = 0

        self.solution = Solution()

    def run(self, solution_id):
        print(solution_id)
        global_var.logger.info(f"Begin to judger {solution_id}")
        solution_data = self.solution.getSolutionData(solution_id)
        # print(solution_data)
        compile_status = Compile().run(
            id=solution_data[0],
            problem=solution_data[1],
            language=solution_data[5],
            code=solution_data[4])
        # print(compile_status)
        if not compile_status:
            global_var.status = True
            return
        data_path = f"./ProblemData/{solution_data[1]}/"
        files = os.listdir(data_path)
        for f_path, dirs, fs in os.walk(data_path):
            for file_item in fs:
                # print(file_item, fs)
                if file_item.endswith('in'):
                    case = file_item.split('.')[0]
                    # print(case)
                    callback = self.testOneCase(
                        solution_id=solution_data[0],
                        problem_id=solution_data[1],
                        case=case,
                        language=solution_data[5],
                        time_limit=solution_data[9],
                        memory_limit=solution_data[10],
                        contest_id=solution_data[3]
                    )
                    if callback == False:
                        global_var.status = True
                        return
        temp_run_result = {
            -6: 0,
            -5: 5,
            -4: 11,
            -3: 6,
            -2: 3,
            -1: 2,
            1: 7,
            2: 9,
            3: 8,
            4: 10,
            5: 12,
            100: 4
        }
        self.solution.doneProblem(
            id=solution_data[0],
            code_length=len(solution_data[4]),
            run_time=self.max_time,
            run_memory=self.max_memory/1024/1024,
            run_result=temp_run_result[int(self.my_result)],
            run_error=self.test_case,
            run_pass_rate=self.run_pass_rate,
            run_all_rate=self.run_all_rate
        )
        global_var.status = True
        global_var.logger.info("All done!!!")
        return

    def testOneCase(self, solution_id, problem_id, case, language, time_limit, memory_limit, contest_id):
        global_var.logger.info(
            f"Judging!!! \nSolution_id:{solution_id}\tProblem_id:{problem_id}\tCase:{case} ")
        try:
            wait_time = 0
            while True:
                memory = self.getMemory()
                if memory >= memory_limit / 5:
                    break
                wait_time += 1
                if wait_time > 15:
                    global_var.logger.info("Memory error!")
                    # 判题机剩余空间过小无法判题
                    global_var.status = True
                    return False
                time.sleep(1)
        except ExecError as e:
            # 判题机空间错误
            global_var.status = True
            return False
        ret = Judger().run(
            language=language,
            timelimit=time_limit,
            memorylimit=memory_limit,
            inputpath=f"./ProblemData/{problem_id}/{case}.in"
        )
        if not ret:
            return False

        global_var.logger.info(str(ret))

        self.max_memory = max(ret["memory"], self.max_memory)
        self.max_time = max(ret["cpu_time"], self.max_time)

        user_output_data = ""
        output_data = ""
        case_data = ""
        if int(contest_id) == -1:
            # print("判断非竞赛题目")
            try:
                input_file = open(f"./ProblemData/{problem_id}/{case}.in", "r")
                case_data = input_file.read(300)
                temp_str = input_file.read(5)
                if temp_str != "":
                    case_data = case_data + '\n......'
                input_file.close()

                output_file = open(
                    f"./ProblemData/{problem_id}/{case}.out", "r")
                output_data = output_file.read(300)
                temp_str = output_file.read(5)
                if temp_str != "":
                    output_data = output_data + '\n......'
                output_file.close()

                user_output_file = open(self.outputpath, "r")
                user_output_data = user_output_file.read(300)
                temp_str = user_output_file.read(5)
                if temp_str != "":
                    user_output_data = user_output_data + '\n......'
                user_output_file.close()
            except:
                ret["result"] = 5

        if ret["result"] != 0:
            if (ret["result"] == 4 and ret["exit_code"] == 127 and ret["signal"] == 0) or (ret["result"] == 4 and ret["exit_code"] == 0 and ret["signal"] == 31):
                if self.my_result == 100:
                    self.my_result = 3
                    self.test_case = case
                    self.my_time = ret["cpu_time"]
                    self.my_memory = ret["memory"]
                # 数据库提交单样例Memory Limit Exceeded
                # print("\n 442 \n")
            else:
                if self.my_result == 100:
                    self.my_result = ret['result']
                    self.test_case = case
                    self.my_time = ret["cpu_time"]
                    self.my_memory = ret["memory"]
                resultstr = "Unknow"
                if ret["result"] == 1 or ret["result"] == 2:
                    resultstr = 'Time Limit Exceeded'
                elif ret["result"] == 3:
                    resultstr = 'Memory Limit Exceeded'
                elif ret["result"] == 4:
                    resultstr = 'Runtime Error'
                elif ret["result"] == 5:
                    resultstr = 'System Error'

                # 数据库提交单组测试的结果
            if contest_id != -1:
                return False
        else:
            # print("\n462\n")
            if os.path.isfile(f"./ProblemData/{problem_id}/spj.cpp"):
                # print("特判")
                global_var.logger.info("Begin to Special judge!!!")
                r = self.specialJudger(
                    problem=problem_id,
                    testin=f"./ProblemData/{problem_id}/{case}.in",
                    testout=f"./ProblemData/{problem_id}/{case}.out",
                    userout=self.outputpath
                )
                if r == 256:
                    result = -3
                elif r == 0:
                    result = 0
                else:
                    result = 5

                if os.path.isfile("./spjmsg.txt"):
                    tmsg = open("./spjmsg.txt", "r", encoding='utf-8')
                    templatemsg = tmsg.read()
                    tmsg.close()
            else:
                result = self.checkAnswer(
                    problem_id=problem_id,
                    filename=case
                )

            if result != 0:
                if self.my_result == 100:
                    self.my_result = result
                    self.test_case = case
                    self.my_time = ret["cpu_time"]
                    self.my_memory = ret["memory"]

                resultstr = "UnKnow"
                if result == -5:
                    resultstr = 'Presentation Error'
                elif result == -3:
                    resultstr = 'Wrong Answer'
                elif result == 5:
                    resultstr = 'System Error'
                # 提交数据库单组样例评测结果

                if contest_id != -1:
                    return False
            else:
                # 单组数据答案正确并提交数据库测试结果
                self.run_pass_rate += 1
                global_var.logger.info(
                    f"{solution_id}: {problem_id}测试数据{case}通过")
            global_var.logger.info("Done one case!")
        self.run_all_rate += 1
        return True

    def checkAnswer(self, problem_id, filename):
        """
        0: Accepted
        -3: Wrong Answer
        5: System Error
        -5: Presentation Error
        """
        result = 0
        global_var.logger.info("Comparing output!!")
        file1 = open(self.outputpath, "r")
        file2 = open(f"./ProblemData/{problem_id}/{filename}.out", "r")

        stdout = ""
        answer = ""

        while True:
            try:
                std = file1.readline()
                ans = file2.readline()

                if std == "" and ans == "":
                    break

                std = std.rstrip()
                ans = ans.rstrip()

                stdout = stdout + std
                answer = answer + ans

                if std != ans:
                    result = -3
            except:
                result = -3
                stdout = "1"
                answer = "0"
        if stdout == answer and result == -3:
            result = -5

        file1.close()
        file2.close()
        del stdout
        del answer
        return result

    def getMemory(self):
        with open('/proc/meminfo') as fd:
            for line in fd:
                if line.startswith('MemAvailable'):
                    free = line.split()[1]
                    fd.close()
                    break
        return int(free)/1024.0

    def specialJudger(self, problem, testin, testout, userout):
        result = os.system(
            f"timeout 10 g++ ./ProblemData/{problem}/spj.cpp -o spj_{self.judger_name}.o -O2 -std=c++14")
        if result:
            return 5
        res = os.system(
            f"timeout 20 ./spj_{self.judger_name}.o {testin} {testout} {userout}")
        return res


if __name__ == "__main__":
    global_var = GlobalVar()
    global_var.setGlobalVar()

    while True:
        # time.sleep(0.1)
        cur = 1
        try:
            data = global_var.client_socket.recv(1024)
            data = data.decode("utf-8")
            if data == "getStatus":
                if global_var.status:
                    global_var.client_socket.send("ok".encode("utf-8"))
                else:
                    global_var.client_socket.send("notOk".encode("utf-8"))
            elif data == "timeOut":
                global_var.logger.error("Judger time error!!!!!")
                # 判题机时间超时
                break
            elif data.find("judger") != -1:
                global_var.status = False
                try:
                    global_var.data_base.ping()
                    print("数据库连接正常")
                except:
                    global_var.reconnect()
                tp = data.split("|")
                cur = tp[1]
                # try:
                #     global_var.cursor.execute(
                #         f"SELECT * FROM `solution` WHERE solution={cur};")
                #     global_var.data_base.commit()
                # except:
                #     global_var.logger.info("Too long no submit, reconnect db!")
                #     global_var.reconnect()
                #     global_var.cursor.execute(
                #         f"SELECT * FROM `solution` WHERE solution={cur};")
                # data = global_var.cursor.fetchone()
                try:
                    global_var.cursor.execute(
                        f"UPDATE solution SET run_result='3' WHERE solution_id = {cur}")
                    global_var.data_base.commit()
                    judger_run = JudgerRun()
                    # judger_run.run(cur)
                    print(cur)
                    t = threading.Thread(
                        target=judger_run.run(cur))
                    t.setDaemon(True)
                    t.start()
                except Exception as e:
                    print(e)
                    global_var.logger.error("database error!!")
                    global_var.data_base.rollback()
                    global_var.status = True
            else:
                global_var.reconnect()
        except socket.error:
            global_var.reconnect()
        except Exception as e:
            global_var.logger.error(repr(e))
            global_var.reconnect()
