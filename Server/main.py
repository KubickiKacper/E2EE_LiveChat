import socket
from client import Client, active_clients

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
        print("connected clients num: " + str(len(active_clients)))
        for c in active_clients:
            print(c.key)
    s.close()
