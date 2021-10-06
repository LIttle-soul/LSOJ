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
                    data = run.run_c()
                elif language == 'cpp':
                    data = run.run_cpp()
                elif language == 'python2':
                    data = run.run_python2()
                elif language == 'python3':
                    data = run.run_python3()
                elif language == 'java':
                    data = run.run_java()
                elif language == 'bash':
                    data = run.run_bash()
                else:
                    return False
                print(f'结果：{data}')
            print(f)
        print(fs)


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


if __name__ == '__main__':
    language_list = [
        'c',
        'cpp',
        'java',
    ]
    code = """#include <bits/stdc++.h>
using namespace std;
#define random(a, b) (rand()%(b-a)+a)

int main()
{
     int i,j,n,x,y,s,c;
     scanf("%d",&n);
    // srand((int)time(0));
    // n = random(2, 100);
    // cout << n << endl;
     for(j=0;j<n;j++)
     {
        scanf("%d%d",&x,&y);
        // x = random(1, 100000);
        // y = random(x, 1000000);
        // cout << x << " " << y << endl;
        s=0;
        i=0;
        c=y-x;
        while(s+i<c)
        {
            s+=i/2;
            i++;
        }
        printf("%d \\n",i);
     }
}"""
    problem = '2119'
    language = 'cpp'
    if write_to_file(code, language):
        if language in language_list:
            if compiler(language):
                runner(problem, language)
            else:
                print('编译错误')
        else:
            runner(problem, language)
