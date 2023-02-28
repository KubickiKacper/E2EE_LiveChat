import socket
import json
import threading
import time

HOST = "127.0.0.1"
PORT = 65432
key=None
nickname=None
connected_flag=False

def initial_connection(client_socket):
    global  connected_flag,key
    data=json.dumps({"symetric_key": key})
    client_socket.send(data.encode())
    connected_flag = not connected_flag

def sender(client_socket):
    print("\n\nYour message: ")
    while True:
        text=input()
        data = json.dumps({"text": text, "nickname": nickname})
        client_socket.send(data.encode())
        print('\x1b[1A\x1b[2K\x1b[1A')
        time.sleep(0.1)


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        if not connected_flag:
            initial_connection(s)

        threading.Thread(target=sender, args=(s,)).start()

        while True:
            data_received = s.recv(1024)
            if not data_received:
                break
            data_received = json.loads(data_received)

            print("\033[A                             \033[A")
            print("\033[A                             \033[A")
            print(f"{data_received['nickname']}: {data_received['text']}")
            print("\nYour message: ")

if __name__ == '__main__':
    key=input("Public key: ")
    nickname=input("Enter your nickname: ")
    run()