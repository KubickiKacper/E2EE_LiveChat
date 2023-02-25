import socket
import json
import threading
import time

HOST = "127.0.0.1"
PORT = 65432
key=None
connected_flag=False

def initial_connection(client_socket):
    global  connected_flag,key
    data=json.dumps({"symetric_key": key})
    client_socket.send(data.encode())
    connected_flag = not connected_flag

def sender(client_socket):
    while True:
        text = input("> ")
        data = json.dumps({"text": text})
        client_socket.send(data.encode())
        print("\033[A                             \033[A")
        time.sleep(0.1)


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        if not connected_flag:
            initial_connection(s)

        threading.Thread(target=sender, args=(s,)).start()

        while True:
            data_recived = s.recv(1024)
            if not data_recived:
                break
            data_recived = json.loads(data_recived)

            print(f"< {data_recived['text']!r}")

if __name__ == '__main__':
    key=input("Public key: ")
    run()