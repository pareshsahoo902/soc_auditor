from abc import ABC, abstractmethod
import json

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, schema: dict = None) -> dict:
        pass

class MockProvider(BaseLLMProvider):
    def generate(self, prompt: str, schema: dict = None) -> dict:
        # Returns structured mock JSON strictly conforming to tasks
        return {
            "finding": "AI Mock Finding: Vague remediation steps detected.",
            "severity": "medium",
            "evidence": ["Snippet: 'we will fix this later'"],
            "confidence": 0.85
        }

class GroqProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, schema: dict = None) -> dict:
        # In a real setup, import groq and use self.model
        # We fallback to mock output here to avoid runtime API dependency
        return {
            "finding": "Groq AI Enrichment Finding.",
            "severity": "low",
            "evidence": ["Data"],
            "confidence": 0.95
        }
