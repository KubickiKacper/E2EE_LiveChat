import uuid

chanel_list = []

class Chanel():

    def __init__(self, chanel_id=uuid.uuid4()):
        self.chanel_id = chanel_id
        self.users = []
