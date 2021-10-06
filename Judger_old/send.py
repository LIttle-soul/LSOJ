import socket
import sys

s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

host = "81.70.218.179"
port = 8086

s.connect((host, port))
while True:
    text = input()
    s.send(text.encode())
    
s.close()

