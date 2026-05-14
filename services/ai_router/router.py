from services.ai_router.provider import MockProvider, GroqProvider

class AIRouter:
    def __init__(self):
        self.provider = MockProvider() # Use Mock by default for MVP

    def route_classification(self, text: str) -> dict:
        prompt = f"Classify the following text into severity and workflow: {text}"
        return self.provider.generate(prompt)

    def route_extraction(self, text: str) -> dict:
        prompt = f"Extract timeline events from: {text}"
        return self.provider.generate(prompt)

    def route_reasoning(self, text: str) -> dict:
        prompt = f"Evaluate the completeness of this RCA: {text}"
        return self.provider.generate(prompt)
