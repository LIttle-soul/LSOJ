import os
import lorun
import pymysql


class Run:
    """
    模块: 程序运行模块
    """

    def __init__(self, temp_file='/temp.out', path=os.getcwd()):
        super(Run, self).__init__()
        self.build_path = path + '/build'
        self.code_path = path + '/code'
        self.temp_path = path + '/temp'
        self.check_dir()
        self.temp_path = self.temp_path + temp_file
        self.RESULT_STR = [
            'Accepted',
            'Presentation Error',
            'Time Limit Exceeded',
            'Memory Limit Exceeded',
            'Wrong Answer',
            'Runtime Error',
            'Output Limit Exceeded',
            'Compile Error',
            'System Error'
        ]
        
    def check_dir(self):
        if not os.path.exists(self.build_path):
            os.makedirs(self.build_path)
        if not os.path.exists(self.code_path):
            os.makedirs(self.code_path)
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)

    def check(self, rst, out_path):
        if rst['result'] == 0:
            f_out = open(out_path)
            f_temp = open(self.temp_path)
            c_rst = lorun.check(f_out.fileno(), f_temp.fileno())
            f_out.close()
            f_temp.close()
            os.remove(self.temp_path)
            if c_rst != 0:
                return {'result': self.RESULT_STR[c_rst]}
        rst['result'] = self.RESULT_STR[rst['result']]
        return rst
    
    def compile_c(self,):
        if os.system(f'gcc {self.code_path}/main.c -o {self.build_path}/main.o -lm') != 0:
            # print('compile failure!')
            return False
        return True

    def compile_cpp(self,):
        code_path = self.code_path
        build_path = self.build_path
        if os.system(f'g++ {code_path}/main.cpp -o {build_path}/main.o') != 0:
            # print('compile failure')
            return False
        return True

    def compile_java(self,):
        if os.system(f'javac {self.code_path}/Main.java -d {self.build_path}/') != 0:
            # print('compile faillure')
            return False
        return True

    def compile_pascal(self,):
        code_path = self.code_path
        build_path = self.build_path
        if os.system(f'fpc {code_path}/main.pas') != 0:
            # print('compile failure')
            return False
        return True    

    def run_c(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': [f'{self.build_path}/main.o'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst

    def run_cpp(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': [f'{self.build_path}/main.o'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst

    def run_java(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['java', f'{self.build_path}/Main'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst

    def run_python2(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['python2', '-u', f'{self.code_path}/main2.py'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst

    def run_python3(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['python3', '-u', f'{self.code_path}/main3.py'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst

    def run_bash(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['sh', f'{self.code_path}/main.sh'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst

    def run_pascal(self, in_path, time_limit=1000, memory_limit=102400):
        f_in = open(in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': [f'{self.code_path}/main'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': time_limit,  # ms
            'memorylimit': memory_limit,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return rst


class SQL:
    """
    模块: 数据库处理模块
    """
    def __init__(self) -> None:
        super(SQL, self).__init__()
        self.db = pymysql.connect(
            host="182.92.71.47",
            user="root",
            port=3306,
            password="cjjdwws144",
            database="jol"
        )
        
    def read(self):
        with self.db.cursor() as cursor:
            sql = """SELECT
	                    solution.solution_id, 
	                    solution.problem_id, 
	                    solution.`language`, 
	                    source_code.source, 
	                    problem.time_limit, 
	                    problem.memory_limit, 
	                    problem.spj
                    FROM
	                    problem
	                INNER JOIN
	                    solution
	                ON 
		                problem.problem_id = solution.problem_id
	                INNER JOIN
	                    source_code
	                ON 
		                source_code.solution_id = solution.solution_id
                    WHERE
	                    solution.problem_id = 1002 AND solution.user_id = '201910101600040'
                    ORDER BY
	                    solution.solution_id;"""
            cursor.execute(sql)
            data = cursor.fetchall()
        return data

    def update(self, solution_id, result, time=0, memory=0, pass_rate=0):
        with self.db.cursor() as cursor:
            sql = f"""
                    UPDATE
	                    solution
                    SET
	                    time={time},
	                    memory={memory},
	                    result={result},
	                    judgetime=NOW(),
	                    pass_rate={pass_rate:.02f}
                    WHERE
	                    solution_id={solution_id};"""
            cursor.execute(sql)
            self.db.commit()
            # print(cursor.fetchall())
        return True

    def insert(self, solution_id, error_info):
        with self.db.cursor() as cursor:
            sql = f"""
                    INSERT INTO
	                    compileinfo
		                (solution_id, error)
	                VALUES
		                ({solution_id}, '{error_info}');"""
            cursor.execute(sql)
            self.db.commit()
            # print(cursor.fetchall())
        return True

    def closed(self):
        self.db.close()

class Code:
    """
    模块: 代码处理模块
    """
    def __init__(self, path=os.getcwd()):
        super(Code, self).__init__()
        # print(path)
        self.data_path = path + '/data'
        self.code_path = path + '/code'
        self.run = Run()

    def runner(self, problem, language, time_limit=1000, memory_limit=102400):
        data_path = f'{self.data_path}/{problem}/'
        for f_path, dirs, fs in os.walk(data_path):
            for f in fs:
                filename = os.path.join(f_path, f)
                if filename.endswith('in'):
                    in_file = filename
                    out_file = filename[:-2] + 'out'
                    print(f'测试点： {f[:-3]}')
                    if language == 'c':
                        data = self.run.run_c(in_file, time_limit, memory_limit)
                    elif language == 'cpp':
                        data = self.run.run_cpp(in_file, time_limit, memory_limit)
                    elif language == 'python2':
                        data = self.run.run_python2(in_file, time_limit, memory_limit)
                    elif language == 'python3':
                        data = self.run.run_python3(in_file, time_limit, memory_limit)
                    elif language == 'java':
                        data = self.run.run_java(in_file, time_limit, memory_limit)
                    elif language == 'bash':
                        data = self.run.run_bash(in_file, time_limit, memory_limit)
                    elif language == 'pascal':
                        data = self.run.run_pascal(in_file, time_limit, memory_limit)
                    else:
                        return False
                    print(f'结果：{self.run.check(data, out_file)}')

    def compiler(self, language):
        if language == 'c':
            return self.run.compile_c()
        elif language == 'cpp':
            return self.run.compile_cpp()
        elif language == 'java':
            return self.run.compile_java()
        elif language == 'pascal':
            return self.run.compile_pascal()
        else:
            return False


    def write_to_file(self, code, language):
        if language == 'c':
            path = f'{self.code_path}/main.c'
        elif language == 'cpp':
            path = f'{self.code_path}/main.cpp'
        elif language == 'python2':
            path = f'{self.code_path}/main2.py'
        elif language == 'python3':
            path = f'{self.code_path}/main3.py'
        elif language == 'java':
            path = f'{self.code_path}/Main.java'
        # elif language == 'go':
        #     path = f'{self.code_path}/main.go'
        # elif language == 'js':
        #     path = f'{self.code_path}/main.js'
        elif language == 'bash':
            path = f'{self.code_path}/main.sh'
        elif language == 'pascal':
            path = f'{self.code_path}/main.pas'
        else:
            return False
        fd = open(path, 'w+')
        fd.write(code)
        fd.close()
        return True


if __name__ == '__main__':
    code_list = {
            0:'c',
            1:'cpp',
            2:'pascal',
            3:'java',
            4:'ruby'
            5:'bash',
            6:'python3',
            7:'python2',
        }
    language_list = [
        'c',
        'cpp',
        'java',
        'pascal',
    ]
    code = Code()
    sql = SQL()
    while True:
        data = sql.read()
        for solution_id, problem_id, language, source, time_limit, memory_limit, spj in data:
            # print(f'提交编号: {solution_id} \t题目编号：{problem_id}\t语言：{language}\n代码：\n{source}\n时间限制:{time_limit}\t空间限制：{memory_limit}\t特判：{spj}\n')
            print(f'\n提交编号：{solution_id}')
            language = code_list[language]
            if code.write_to_file(source, language):
                if language in language_list:
                    if code.compiler(language):
                        code.runner(problem_id, language, time_limit*1000, memory_limit*1024)
                    else:
                        print('编译错误')
                else:
                    code.runner(problem_id, language, time_limit*1000, memory_limit*1024)
            else:
                print('系统错误')
        sql.closed()
        break