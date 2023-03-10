import socket
import json
import threading
import time

HOST = "127.0.0.1"
PORT = 65432
chanel=None
nickname=None


def initial_connection(client_socket):
    data=json.dumps({"chanel": chanel})
    client_socket.send(data.encode())

def sender(client_socket):
    print("\n\nYour message: ")
    while True:
        text=input()
        data = json.dumps({"text": text, "nickname": nickname})
        client_socket.send(data.encode())
        print('\x1b[1A\x1b[2K\x1b[1A')
        time.sleep(0.1)

def create_chanel(client_socket):
    global chanel

    data = json.dumps({"create_chanel": True})
    client_socket.send(data.encode())
    print("sending")

    while True:
        data_received = client_socket.recv(1024)
        if not data_received:
            break
        data_received = json.loads(data_received)
        chanel = data_received["chanel_id"]
        print(chanel)

        return


def run(input_nickname, input_chanel = None, create_chanel_flag = False):
    global chanel, nickname
    chanel, nickname = input_chanel, input_nickname

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        if create_chanel_flag is True:
            create_chanel(s)
        else:
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