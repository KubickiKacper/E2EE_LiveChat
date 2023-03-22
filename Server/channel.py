import uuid

channel_list = []

class Channel():

    def __init__(self, channel_id=uuid.uuid4()):
        self.channel_id = channel_id
        self.users = []
