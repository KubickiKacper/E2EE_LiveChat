import threading
import json
import channel


class Client(threading.Thread):
    def __init__(self, client_conn, client_addr):
        super(Client, self).__init__()
        self.client_conn=client_conn
        self.client_addr=client_addr
        self.client_channel=None

    def run(self):
        while True:
            data = self.client_conn.recv(1024)
            if not data:
                break
            data=json.loads(data)

            try:
                if data["text"]:
                    print(data)
                    clients = self.client_channel.users
                    data=json.dumps(data)
                    for c in clients:
                        c.send_msg(data)
            except:
                pass

            try:
                if data["channel"]:
                    ch = [ch for ch in channel.channel_list if str(ch.channel_id) == data["channel"]]
                    self.client_channel = ch[0]
                    self.client_channel.users.append(self)
            except:
                pass

            try:
                if data["create_channel"]:
                    print(data)
                    ch=channel.Channel()
                    self.client_channel = ch
                    channel.channel_list.append(ch)
                    self.client_channel.users.append(self)
                    data_to_send = json.dumps({"channel_id": str(self.client_channel.channel_id)})
                    self.client_conn.sendall(data_to_send.encode())
            except:
                pass

        self.client_conn.close()

    def send_msg(self, data):
        self.client_conn.sendall(data.encode())
        print("sending")