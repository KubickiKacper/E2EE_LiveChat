import threading
import json

active_clients=[]

class Client(threading.Thread):
    def __init__(self, client_conn, client_addr):
        super(Client, self).__init__()
        self.client_conn=client_conn
        self.client_addr=client_addr
        self.key=None
        active_clients.append(self)

    def run(self):
        while True:
            data = self.client_conn.recv(1024)
            if not data:
                break
            data=json.loads(data)

            try:
                if data["text"]:
                    print(data["text"])
                    data=json.dumps(data)
                    clients=self.find_same_key_clients()
                    print("clients: ")
                    print(active_clients)

                    for c in clients:
                        c.send_msg(data)

            except:
                if data["symetric_key"]:
                    self.key=data["symetric_key"]

        self.client_conn.close()

    def find_same_key_clients(self):
        return [ac for ac in active_clients if ac.key == self.key]

    def send_msg(self,data):
        print("Sending to " +str(self.key))
        self.client_conn.sendall(data.encode())