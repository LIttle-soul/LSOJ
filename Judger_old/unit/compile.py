import os


class Compile:
    def __init__(self):
        super(Compile, self).__init__()
        self.code_path = os.getcwd() + '/code'
        self.build_path = os.getcwd() + '/build'

    def compile_c(self,):
        if os.system(f'gcc {self.code_path}/main.c -o {self.build_path}/main.o') != 0:
            print('compile failure!')
            return False
        return True

    def compile_cpp(self,):
        code_path = self.code_path
        build_path = self.build_path
        if os.system(f'g++ {code_path}/main.cpp -o {build_path}/main.o') != 0:
            print('compile failure')
            return False
        return True

    def compile_java(self,):
        if os.system(f'javac {self.code_path}/Main.java -d {self.build_path}/') != 0:
            print('compile faillure')
            return False
        return True
