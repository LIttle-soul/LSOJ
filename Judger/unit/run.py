import os
import lorun


class Run:
    def __init__(self, in_file, out_file, temp_file='temp.out'):
        super(Run, self).__init__()
        self.build_path = './build'
        self.code_path = './code'
        self.in_path = in_file
        self.out_path = out_file
        self.temp_path = f'./temp/{temp_file}'
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

    def check(self, rst):
        if rst['result'] == 0:
            f_out = open(self.out_path)
            f_temp = open(self.temp_path)
            c_rst = lorun.check(f_out.fileno(), f_temp.fileno())
            f_out.close()
            f_temp.close()
            os.remove(self.temp_path)
            if c_rst != 0:
                return {'result': self.RESULT_STR[c_rst]}
        rst['result'] = self.RESULT_STR[rst['result']]
        return rst

    def run_c(self):
        f_in = open(self.in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': [f'{self.build_path}/main.o'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': 1000,  # ms
            'memorylimit': 102400,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return self.check(rst)

    def run_cpp(self):
        f_in = open(self.in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': [f'{self.build_path}/main.o'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': 1000,  # ms
            'memorylimit': 102400,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return self.check(rst)

    def run_java(self):
        f_in = open(self.in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['java', f'{self.build_path}/Main'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': 1000,  # ms
            'memorylimit': 204800,  # kb
        }
        rst = lorun.run(run_cfg)
        f_in.close()
        f_temp.close()
        return self.check(rst)

    def run_python2(self):
        f_in = open(self.in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['python2', '-u', f'{self.code_path}/main2.py'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': 1000,  # ms
            'memorylimit': 102400,  # kb
        }
        try:
            rst = lorun.run(run_cfg)
        except SyntaxError:
            return {'result': self.RESULT_STR[7]}
        f_in.close()
        f_temp.close()
        return self.check(rst)

    def run_python3(self):
        f_in = open(self.in_path)
        f_temp = open(self.temp_path, 'w')
        run_cfg = {
            'args': ['python3', '-u', f'{self.code_path}/main3.py'],
            'fd_in': f_in.fileno(),
            'fd_out': f_temp.fileno(),
            'timelimit': 1000,  # ms
            'memorylimit': 102400,  # kb
        }
        try:
            rst = lorun.run(run_cfg)
        except SyntaxError:
            return {'result': self.RESULT_STR[7]}
        f_in.close()
        f_temp.close()
        return self.check(rst)
