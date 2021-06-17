import os
from unit.compile import Compile
from unit.run import Run


def runner(problem, language):
    path = os.getcwd()
    path = f'{path}/data/{problem}/'
    for f_path, dirs, fs in os.walk(path):
        for f in fs:
            filename = os.path.join(f_path, f)
            if filename.endswith('in'):
                in_file = filename
                out_file = filename[:-2] + 'out'
                print(f'测试点： {f[:-3]}')
                run = Run(in_file, out_file)
                if language == 'c':
                    print(run.run_c())
                elif language == 'cpp':
                    print(run.run_cpp())
                elif language == 'python2':
                    print(run.run_python2())
                elif language == 'python3':
                    print(run.run_python3())
                elif language == 'java':
                    print(run.run_java())
                elif language == 'bash':
                    print(run.run_bash())
                else:
                    return False


def compiler(language):
    compiled = Compile()
    if language == 'c':
        return compiled.compile_c()
    elif language == 'cpp':
        return compiled.compile_cpp()
    elif language == 'java':
        return compiled.compile_java()
    else:
        return True


def write_to_file(coder, language):
    path = os.getcwd()
    if language == 'c':
        path = f'{path}/code/main.c'
    elif language == 'cpp':
        path = f'{path}/code/main.cpp'
    elif language == 'python2':
        path = f'{path}/code/main2.py'
    elif language == 'python3':
        path = f'{path}/code/main3.py'
    elif language == 'java':
        path = f'{path}/code/Main.java'
    elif language == 'go':
        path = f'{path}/code/main.go'
    elif language == 'js':
        path = f'{path}/code/main.js'
    elif language == 'bash':
        path = f'{path}/code/main.sh'
    else:
        return False
    fd = open(path, 'w+')
    fd.write(code)
    fd.close()
    return True


def replace_word(s):
    return s.replace('<br\>', '\\n')

if __name__ == '__main__':
    language_list = [
        'c',
        'cpp',
        'java',
    ]
    code = """#include<bits/stdc++.h>
using namespace std;

int main(){
    cout << "Hello, World!<br\>";
    return 0;
}"""
    problem = '2'
    language = 'python3'
    if write_to_file(code, language):
        if language in language_list:
            if compiler(language):
                runner(problem, language)
            else:
                print('编译错误')
        else:
            runner(problem, language)
