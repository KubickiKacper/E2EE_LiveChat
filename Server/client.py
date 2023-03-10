import threading
import json
import chanel


class Client(threading.Thread):
    def __init__(self, client_conn, client_addr):
        super(Client, self).__init__()
        self.client_conn=client_conn
        self.client_addr=client_addr
        self.client_chanel=None

    def run(self):
        while True:
            data = self.client_conn.recv(1024)
            if not data:
                break
            data=json.loads(data)

            try:
                if data["text"]:
                    print(data)
                    clients = self.client_chanel.users
                    data=json.dumps(data)
                    for c in clients:
                        c.send_msg(data)
            except:
                pass

            try:
                if data["chanel"]:
                    ch = [ch for ch in chanel.chanel_list if str(ch.chanel_id) == data["chanel"]]
                    self.client_chanel = ch[0]
                    self.client_chanel.users.append(self)
            except:
                pass

            try:
                if data["create_chanel"]:
                    print(data)
                    ch=chanel.Chanel()
                    self.client_chanel = ch
                    chanel.chanel_list.append(ch)
                    self.client_chanel.users.append(self)
                    data_to_send = json.dumps({"chanel_id": str(self.client_chanel.chanel_id)})
                    self.client_conn.sendall(data_to_send.encode())
            except:
                pass

        self.client_conn.close()

    def send_msg(self, data):
        self.client_conn.sendall(data.encode())
        print("sending")