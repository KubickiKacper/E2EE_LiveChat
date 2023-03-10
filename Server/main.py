import socket
from client import Client

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('waiting for connection')
    while True:
        conn, addr = s.accept()
        print('connected')
        new_client=Client(conn,addr).start()
    s.close()
