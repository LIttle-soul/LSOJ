cd /Judger
nohup python serve.py > serve.log 2>&1 &
nohup python main.py > client.log 2>&1 &