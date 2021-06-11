class Check:
    def __init__(self):
        super(Check, self).__init__()
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

    def check(self, out_file, temp_file='temp.out'):
        pass