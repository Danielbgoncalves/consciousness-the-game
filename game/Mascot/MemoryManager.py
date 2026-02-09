class MemoryManager:
    def __init__(self):
        self.memory = []

    def add_memory(self, memory_text):
        if memory_text not in self.memory:
            self.memory.append(memory_text)

    def get_memorys(self):
        return self.memory
    
    def summarize_memories(self):
        if not self.memory:
            return "Nenhuma memória registrada"
        else:
            summary = "\n".join(f"- {m}" for m in self.memory)
            return f"Memórias até agora:\n{summary}"