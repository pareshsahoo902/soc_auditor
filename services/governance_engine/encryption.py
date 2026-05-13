import base64
import os

class MockEncryption:
    @staticmethod
    def encrypt(data: str) -> str:
        # Mock encryption, e.g., base64 wrapping
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def decrypt(data: str) -> str:
        return base64.b64decode(data.encode()).decode()
