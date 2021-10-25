from shutil import ExecError
import pymysql.cursors
import socket
import json
import time
import threading
from util import _judger
import os
import time
import logging
from file_cliect import FileClient


class GlobalVar:
    def __init__(self):
        # 判题机属性
        self.status = False
        self.name = None
        self.host = None
        self.token = None

        # 服务端地址
        self.serve_host = None
        self.serve_port = None

        # 判题机运行环境
        self.c_path = None
        self.cpp_path = None
        self.java_path = None
        self.javac_path = None
        self.python2_path = None
        self.python3_path = None
        self.bash_path = None
        self.pascal_path = None

        # 数据库相关变量
        self.data_base = None
        self.cursor = None

        # Socket相关变量
        self.client_socket = None

        # 运行日志
        self.logger = None

        # 运行文件储存位置
        self.problem_data_path = "./ProblemData/"
        self.run_data_path = "./RunData/"
        self.log_path = "./logs/"

        # 配置文件
        self.setting_file = None

    # 运行日志初始化
    def setLogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler(f"{self.log_path}judger.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

        self.logger.info("Start print log")

    # 内部变量初始化
    def setGlobalVar(self):

        # 读取配置文件
        jsonfile = open("./config/client_setting.json", 'r')
        judger_json = json.loads(jsonfile.read())
        jsonfile.close()
        self.setting_file = judger_json

        self.name = socket.gethostname() or judger_json["client_name"]
        self.host = socket.gethostbyname(
            socket.gethostname()) or judger_json["client_host"]

        # 设置日志
        self.log_path = f"{judger_json['log_path']}{self.name}/"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        self.setLogger()

        # 设置运行目录
        self.problem_data_path = judger_json["problem_data_path"]
        self.run_data_path = judger_json["run_data_path"] + self.name + '/'
        if not os.path.exists(self.run_data_path):
            os.makedirs(self.run_data_path)

        # 设置相关配置
        self.logger.info(f"Judger name: {self.name}\nJudger host: {self.host}")

        self.serve_host = judger_json["server_host"]
        self.serve_port = judger_json["server_port"]

        self.c_path = judger_json["c_path"]
        self.cpp_path = judger_json["cpp_path"]
        self.java_path = judger_json["java_path"]
        self.javac_path = judger_json["javac_path"]
        self.python2_path = judger_json["python2_path"]
        self.python3_path = judger_json["python3_path"]
        self.bash_path = judger_json["bash_path"]
        self.pascal_path = judger_json["pascal_path"]

        self.logger.info("Connecting database !")
        self.data_base = pymysql.connect(
            host=judger_json["db_host"],
            port=judger_json["db_port"],
            user=judger_json["db_user"],
            password=judger_json["db_password"],
            database=judger_json["db_database"],
            charset='utf8mb4'
        )
        self.cursor = self.data_base.cursor()
        self.logger.info("Connect db succeed!")

        self.logger.info("Connecting judger server!")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.serve_host, self.serve_port))
        self.logger.info("Connect judger server succeed!")

        self.status = True

    # 数据库重连
    def reconnect_database(self):
        try:
            self.data_base = pymysql.connect(
                host=self.setting_file["db_host"],
                port=self.setting_file["db_port"],
                user=self.setting_file["db_user"],
                password=self.setting_file["db_password"],
                database=self.setting_file["db_database"],
                charset='utf8mb4'
            )
            self.cursor = self.data_base.cursor()
            self.status = True
        except Exception as e:
            self.logger.error("Connect data base failed!")
            self.logger.error(repr(e))

    # 服务端重连
    def reconnect_socket(self):
        try:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.serve_host, self.serve_port))
        except Exception as e:
            self.logger.error("Connect socket failed!")
            self.logger.error(repr(e))


class Solution:
    def __init__(self):
        self.name = global_var.name
        self.host = global_var.host
        self.data_base = global_var.data_base
        self.cursor = global_var.cursor

    # 获取提交数据
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
        return self.cursor.fetchone()

    # 编译错误
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

    # 提交判题数据
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

    # 题目重判
    def resetProblem(self, id):
        sql = f"""UPDATE
                    solution 
                SET 
                    run_result = '1'
                WHERE
	                solution_id = {id};"""
        self.cursor.execute(sql)
        self.data_base.commit()

    # 开始判题
    def getProblem(self, id):
        sql = f"""UPDATE
                    solution 
                SET 
                    run_result = '3'
                WHERE
	                solution_id = {id};"""
        self.cursor.execute(sql)
        self.data_base.commit()


# 程序运行
class Judger:
    def __init__(self):
        self.solution = Solution()
        self.name = global_var.name
        self.run_data_path = global_var.run_data_path
        self.output_path = f"{global_var.run_data_path}output.out"
        self.error_path = f"{global_var.run_data_path}error.out"

    def run(self, id, language, timelimit, memorylimit, inputpath):
        if language == 0:
            return self.judgeC(timelimit, memorylimit, inputpath)
        elif language == 1:
            return self.judgeCPP(timelimit, memorylimit, inputpath)
        elif language == 2:
            return self.judgeJava(timelimit*3, memorylimit, inputpath)
        elif language == 3:
            return self.judgePython2(timelimit, memorylimit, inputpath)
        elif language == 4:
            return self.judgePython3(timelimit, memorylimit, inputpath)
        elif language == 5:
            return self.judgeBash(timelimit, memorylimit, inputpath)
        elif language == 6:
            return self.judgePascal(timelimit, memorylimit, inputpath)
        else:
            self.solution.compileError(id=id, message="语言选择错误")
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
                           exe_path=f"{self.run_data_path}{self.name}.o",
                           input_path=inputpath,
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=[],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
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
                           exe_path=f"{self.run_data_path}{self.name}.o",
                           input_path=inputpath,
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=[],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
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
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=[f"{self.run_data_path}{self.name}.py"],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
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
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=[f"{self.run_data_path}{self.name}.py"],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
                           # can be None
                           seccomp_rule_name="general",
                           uid=0,
                           gid=0
                           )

    def judgeJava(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=global_var.java_path,
                           input_path=inputpath,
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=["-cp", f"{self.run_data_path}{self.name}", "-Djava.security.policy==policy",
                                 "-Djava.awt.headless=true", "Main"],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
                           # can be None
                           seccomp_rule_name=None,
                           memory_limit_check_only=1,
                           uid=0,
                           gid=0
                           )

    def judgeBash(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=global_var.bash_path,
                           input_path=inputpath,
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=[f"{self.run_data_path}{self.name}.sh"],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
                           # can be None
                           seccomp_rule_name=None,
                           uid=0,
                           gid=0
                           )

    def judgePascal(self, timelimit, memorylimit, inputpath):
        return _judger.run(max_cpu_time=timelimit,
                           max_real_time=timelimit*10,
                           max_memory=memorylimit * 1024 * 1024,
                           max_process_number=10,
                           max_output_size=32 * 1024 * 1024,
                           max_stack=32 * 1024 * 1024,
                           # five args above can be _judger.UNLIMITED
                           exe_path=f"{self.run_data_path}{self.name}_pascal",
                           input_path=inputpath,
                           output_path=self.output_path,
                           error_path=self.error_path,
                           args=[],
                           # can be empty list
                           env=[],
                           log_path=f"{self.run_data_path}run_log.log",
                           # can be None
                           seccomp_rule_name="general",
                           memory_limit_check_only=1,
                           uid=0,
                           gid=0
                           )


# 程序编译
class Compile:
    def __init__(self):
        self.name = global_var.name
        self.run_data_path = global_var.run_data_path
        self.solution = Solution()

    def run(self, id, problem, language, code):
        language = int(language)
        if language == 0:
            return self.compileC(id, problem, code)
        elif language == 1:
            return self.compileCPP(id, problem, code)
        elif language == 2:
            return self.compileJava(id, problem, code)
        elif language == 3 or language == 4:
            return self.compilePython(id, problem, code)
        elif language == 5:
            return self.compileBash(id, problem, code)
        elif language == 6:
            return self.compilePascal(id, problem, code)
        else:
            self.solution.compileError(id=id, message="语言选择错误")
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
        file = open(f'{self.run_data_path}{self.name}.c',
                    'w', encoding='utf-8')
        file.write(code)
        file.close()
        cmd = f'timeout 10 {global_var.c_path} {self.run_data_path}{self.name}.c -fmax-errors=3 -o {self.run_data_path}{self.name}.o -O2 -std=c11 2>{self.run_data_path}{self.name}ce.txt'
        result = os.system(cmd)
        if result:
            try:
                filece = open(f"{self.run_data_path}{self.name}ce.txt", "r")
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
            # print(id, code, self.name, problem)
            return False
        # print(id, code, self.name, problem)
        return True

    def compileCPP(self, id, problem, code):
        file = open(f'{self.run_data_path}{self.name}.cpp',
                    'w', encoding='utf-8')
        file.write(code)
        file.close()
        cmd = f'timeout 10 {global_var.cpp_path} {self.run_data_path}{self.name}.cpp -fmax-errors=3 -o {self.run_data_path}{self.name}.o -O2 -std=c++14 2>{self.run_data_path}{self.name}ce.txt'
        result = os.system(cmd)
        if result:
            try:
                filece = open(f"{self.run_data_path}{self.name}ce.txt", "r")
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
            # print(id, code, self.name, problem)
            return False
        # print(id, code, self.name, problem)
        return True

    def compilePython(self, id, problem, code):
        wo = self.checkSensitiveWord(code)
        if wo != "0":
            self.solution.compileError(
                id=id, message="Your code has sensitive words "+wo)
            global_var.status = True
            return False
        file = open(f"{self.run_data_path}{self.name}.py",
                    "w", encoding='utf-8')
        # file.write("import sys\nblacklist = ['importlib','traceback','os']\nfor mod in blacklist:\n    i = __import__(mod)\n    sys.modules[mod] = None\ndel __builtins__.__dict__['eval']\ndel __builtins__.__dict__['locals']\ndel __builtins__.__dict__['open']\n" +code)
        file.write(code)
        file.close()
        return True

    def compileJava(self, id, problem, code):
        file = open(f"{self.run_data_path}Main.java", "w", encoding='utf-8')
        file.write(code)
        file.close()

        if not os.path.exists(f"{self.run_data_path}{self.name}"):
            os.makedirs(f"{self.run_data_path}{self.name}")

        result = os.system(
            f"{global_var.javac_path} {self.run_data_path}Main.java -d {self.run_data_path}{self.name} 2>{self.run_data_path}{self.name}ce.txt")

        if result:
            try:
                filece = open(f"{self.run_data_path}{self.name}ce.txt", "r")
                msg = str(filece.read())
                filece.close()
                self.solution.compileError(id=id, message=msg)
                global_var.statue = True
            except:
                msg = str("Fatal Compile error!")
                self.solution.compileError(id=id, message=msg)
                global_var.statue = True
            return False
        return True

    def compileBash(self, id, problem, code):
        file = open(f"{self.run_data_path}{self.name}.sh",
                    "w", encoding='utf-8')
        file.write(code)
        file.close()
        return True

    def compilePascal(self, id, problem, code):
        file = open(f'{self.run_data_path}{self.name}_pascal.pas',
                    'w', encoding='utf-8')
        file.write(code)
        file.close()
        cmd = f'{global_var.pascal_path} {self.run_data_path}{self.name}_pascal.pas  2>{self.run_data_path}{self.name}ce.txt'
        result = os.system(cmd)
        if result:
            try:
                filece = open(f"{self.run_data_path}{self.name}ce.txt", "r")
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
            # print(id, code, self.name, problem)
            return False
        # print(id, code, self.name, problem)
        return True


class JudgerRun:
    def __init__(self):
        self.solution = Solution()
        self.name = global_var.name
        self.run_data_path = global_var.run_data_path
        self.output_path = f"{global_var.run_data_path}output.out"
        self.error_path = f"{global_var.run_data_path}error.out"

        self.max_memory = 0
        self.max_time = 0

        self.my_result = 100
        self.test_case = ""
        self.my_time = 0
        self.my_memory = 0

        self.run_pass_rate = 0
        self.run_all_rate = 0

        self.temp_run_result = {
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
            6: 1,
            100: 4
        }

    def run(self, solution_id):
        global_var.logger.info(f"Begin to judger {solution_id}")
        solution_data = self.solution.getSolutionData(solution_id)
        compile_status = Compile().run(
            id=solution_data[0],
            problem=solution_data[1],
            language=solution_data[5],
            code=solution_data[4])
        if not compile_status:
            global_var.status = True
            return
        self.solution.doneProblem(
            id=solution_data[0],
            code_length=0,
            run_time=0,
            run_memory=0,
            run_result=2,
            run_error='验证判题数据中',
            run_pass_rate=0,
            run_all_rate=0
        )
        if not FileClient().handle_tcp_file(problem_id=solution_data[1]):
            self.solution.doneProblem(
                id=solution_data[0],
                code_length=0,
                run_time=0,
                run_memory=0,
                run_result=12,
                run_error='判题数据验证失败',
                run_pass_rate=0,
                run_all_rate=0
            )
            global_var.status = True
            return
        else:
            self.solution.doneProblem(
                id=solution_data[0],
                code_length=0,
                run_time=0,
                run_memory=0,
                run_result=2,
                run_error='判题数据验证成功',
                run_pass_rate=0,
                run_all_rate=0
            )
        data_path = f"{global_var.problem_data_path}{solution_data[1]}/"
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
                        self.solution.doneProblem(
                            id=solution_data[0],
                            code_length=len(solution_data[4]),
                            run_time=self.max_time,
                            run_memory=self.max_memory/1024/1024,
                            run_result=self.temp_run_result[int(
                                self.my_result)],
                            run_error=self.test_case,
                            run_pass_rate=self.run_pass_rate,
                            run_all_rate=self.run_all_rate
                        )
                        global_var.status = True
                        return

        self.solution.doneProblem(
            id=solution_data[0],
            code_length=len(solution_data[4]),
            run_time=self.max_time,
            run_memory=self.max_memory/1024/1024,
            run_result=self.temp_run_result[int(self.my_result)],
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
                    self.my_result = 6
                    # 判题机剩余空间过小无法判题
                    global_var.status = True
                    return False
                time.sleep(1)
        except ExecError as e:
            # 判题机空间错误
            self.solution.resetProblem(id=solution_id)
            global_var.status = True
            return False
        ret = Judger().run(
            id=solution_id,
            language=language,
            timelimit=time_limit,
            memorylimit=memory_limit,
            inputpath=f"{global_var.problem_data_path}{problem_id}/{case}.in"
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
                input_file = open(
                    f"{global_var.problem_data_path}{problem_id}/{case}.in", "r")
                case_data = input_file.read(300)
                temp_str = input_file.read(5)
                if temp_str != "":
                    case_data = case_data + '\n......'
                input_file.close()

                output_file = open(
                    f"{global_var.problem_data_path}{problem_id}/{case}.out", "r")
                output_data = output_file.read(300)
                temp_str = output_file.read(5)
                if temp_str != "":
                    output_data = output_data + '\n......'
                output_file.close()

                user_output_file = open(self.output_path, "r")
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
            if os.path.isfile(f"{global_var.problem_data_path}{problem_id}/spj.cpp"):
                # print("特判")
                global_var.logger.info("Begin to Special judge!!!")
                r = self.specialJudger(
                    problem=problem_id,
                    testin=f"{global_var.problem_data_path}{problem_id}/{case}.in",
                    testout=f"{global_var.problem_data_path}{problem_id}/{case}.out",
                    userout=self.output_path
                )
                if r == 256:
                    result = -3
                elif r == 0:
                    result = 0
                else:
                    result = 5

                if os.path.isfile(f"{global_var.problem_data_path}spjmsg.txt"):
                    tmsg = open(
                        f"{global_var.problem_data_path}spjmsg.txt", "r", encoding='utf-8')
                    templatemsg = tmsg.read()
                    tmsg.close()
            else:
                result = self.checkAnswer(
                    problem_id=problem_id,
                    filename=case
                )
            # print(result)
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
        file1 = open(self.output_path, "r")
        file2 = open(
            f"{global_var.problem_data_path}{problem_id}/{filename}.out", "r")

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
            f"timeout 10 {global_var.cpp_path} {global_var.problem_data_path}{problem}/spj.cpp -o {self.run_data_path}spj_{self.name}.o -O2 -std=c++14")
        if result:
            return 5
        res = os.system(
            f"timeout 20 {self.run_data_path}spj_{self.name}.o {testin} {testout} {userout}")
        return res


if __name__ == "__main__":
    global_var = GlobalVar()
    global_var.setGlobalVar()
    solution_var = Solution()

    while True:
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
                    # print("数据库连接正常")
                except:
                    global_var.data_base.close()
                    global_var.reconnect_database()
                tp = data.split("|")
                cur = tp[1]
                try:
                    solution_var.getProblem(id=cur)
                    judger_run = JudgerRun()
                    # print(cur)
                    t = threading.Thread(
                        target=judger_run.run(cur))
                    t.setDaemon(True)
                    t.start()
                except BrokenPipeError:
                    global_var.data_base.close()
                    global_var.reconnect_database()
                except Exception as e:
                    print(e)
                    solution_var.resetProblem(id=cur)
                    global_var.logger.error("database error!!")
                    global_var.data_base.rollback()
                    global_var.status = True
            else:
                global_var.reconnect_socket()
        except BrokenPipeError:
            global_var.data_base.close()
            global_var.reconnect_database()
        except socket.error:
            print(socket.error)
            solution_var.resetProblem(id=cur)
            global_var.reconnect_socket()
        except Exception as e:
            solution_var.resetProblem(id=cur)
            global_var.logger.error(repr(e))
            global_var.reconnect_socket()
            global_var.reconnect_database()
