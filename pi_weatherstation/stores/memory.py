import asyncio


class MemoryStore:
    def __init__(self):
        self.stored_data = {}
        self.ready = asyncio.Event()

    def update(self, data):
        self.stored_data.update(data)
        self.ready.set()
        self.ready.clear()

    def get(self, *args, **kwargs):
        return self.stored_data.get(*args, **kwargs)


store = MemoryStore()
