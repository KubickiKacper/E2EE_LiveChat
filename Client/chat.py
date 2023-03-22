import socket
import json
import threading
import time
from cryptography.fernet import Fernet

HOST = "127.0.0.1"
PORT = 65432
channel=None
nickname=None
key=None

def initial_connection(client_socket):
    data=json.dumps({"channel": channel})
    client_socket.send(data.encode())

def sender(client_socket):
    global key

    print("\n\nYour message: ")
    while True:
        text=input()
        data = json.dumps({"text": str(key.encrypt(text.encode())), "nickname": str(key.encrypt(nickname.encode()))})
        client_socket.send(data.encode())
        print('\x1b[1A\x1b[2K\x1b[1A')
        time.sleep(0.1)

def create_channel(client_socket):
    global channel

    data = json.dumps({"create_channel": True})
    client_socket.send(data.encode())

    while True:
        data_received = client_socket.recv(1024)
        if not data_received:
            break
        data_received = json.loads(data_received)
        channel = data_received["channel_id"]
        print("Your channel: ")
        print(channel)

        return


def run(input_nickname, crypto_key, input_channel = None, create_channel_flag = False):
    global nickname, key, channel
    nickname, channel = input_nickname, input_channel
    key=Fernet(crypto_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        if create_channel_flag is True:
            create_channel(s)
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

            try:
                decrypted_nickname=key.decrypt(eval(data_received['nickname'])).decode()
                decrypted_text=key.decrypt(eval(data_received['text'])).decode()
                print(f"{decrypted_nickname}: {decrypted_text}")
            except:
                print("Message is impossible to decrypt. Check your symmetric key.")

            print("\nYour message: ")