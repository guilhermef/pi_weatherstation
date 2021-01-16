class MemoryStore:
    def __init__(self):
        self.stored_data = {}

    def update(self, data):
        self.stored_data.update(data)


store = MemoryStore()
