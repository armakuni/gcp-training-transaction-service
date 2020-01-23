class MockPubSubClient:
    def __init__(self):
        self.msg_published = None

    def send_message(self, message):
        self.msg_published = message
