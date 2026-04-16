from models.sentiment_model import AdvancedSentimentModel


class SentimentAnalyzer:
    def __init__(self):
        self.model = AdvancedSentimentModel()

    def analyze(self, text: str) -> dict:
        result = self.model.predict(text)

        # Normalize to 3 main classes for UI
        emotion = result["emotion"]

        if emotion in ["joy", "love"]:
            sentiment = "positive"
        elif emotion in ["anger", "sadness", "fear"]:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "emotion": emotion,
            "confidence": result["confidence"],
            "intensity": result["intensity"]
        }