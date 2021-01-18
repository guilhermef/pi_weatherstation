class MemoryStore:
    def __init__(self):
        self.stored_data = {}

    def update(self, data):
        self.stored_data.update(data)

    def get(self, *args, **kwargs):
        return self.stored_data.get(*args, **kwargs)


store = MemoryStore()
