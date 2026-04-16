class MemoryManager:
    def __init__(self):
        self.history = []

    def add(self, role, message):
        self.history.append({"role": role, "content": message})

    def get_context(self, limit=5):
        return self.history[-limit:]