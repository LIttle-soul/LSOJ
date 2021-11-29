# LSOJ 开发文档

- 判题机目录映射

```sh
  /home/Judger/JudgerClient -> /Judger/Client
  /www/wwwroot/LSOJ/JudgerClient -> /Judger
```

- 无终端后台启动命令

```sh
  nohup python serve.py > ./logs/server.log 2>&1 &
  nohup python file_serve.py > ./logs/server.log 2>&1 &
  nohup python client.py > ./logs/server.log 2>&1 &
```

cd Judger
