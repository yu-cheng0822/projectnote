import requests


class LocalLLM:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:1.5b"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]