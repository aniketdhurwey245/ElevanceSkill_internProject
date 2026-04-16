from models.sentiment_model import AdvancedSentimentModel
from core.memory_manager import MemoryManager
from core.response_generator import AdvancedResponseGenerator

class AdvancedChatbot:

    def __init__(self):
        self.sentiment = AdvancedSentimentModel()
        self.memory = MemoryManager()
        self.generator = AdvancedResponseGenerator()

    def process(self, query):
        emotion = self.sentiment.predict(query)

        self.memory.add("user", query)

        response = self.generator.generate(
            query,
            emotion,
            self.memory.get_context()
        )

        self.memory.add("assistant", response)

        return {
            "response": response,
            "emotion": emotion
        }