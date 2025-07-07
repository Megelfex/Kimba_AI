
class KimbaMemory:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.log = []

    def remember(self, message):
        self.log.append(message)

    def recall(self):
        return self.log
