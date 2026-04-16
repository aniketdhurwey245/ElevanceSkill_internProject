from transformers import pipeline

class AdvancedSentimentModel:
    def __init__(self):
        self.model = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )

    def predict(self, text: str):
        results = self.model(text)[0]

        # Sort emotions
        sorted_res = sorted(results, key=lambda x: x['score'], reverse=True)

        top_emotion = sorted_res[0]["label"]
        confidence = sorted_res[0]["score"]

        intensity = "low"
        if confidence > 0.75:
            intensity = "high"
        elif confidence > 0.5:
            intensity = "medium"

        return {
            "emotion": top_emotion,
            "confidence": confidence,
            "intensity": intensity
        }