import requests
import json

class NLPInterpreter:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model="mistral"):
        self.url = ollama_url
        self.model = model

    def interpret_question(self, question):
        prompt = (
            "You are an intelligent assistant that extracts the user's intent and company name from a financial question.\n\n"
            "Return a JSON object with:\n"
            "{\n"
            "  \"intent\": one of [\"ownership_query\", \"authorization_query\", \"other\"],\n"
            "  \"company\": extracted company name or null\n"
            "}\n\n"
            "Respond ONLY with valid JSON. No comments, no explanation.\n\n"
            "Examples:\n"
            "- \"Who owns Twinize?\" → {\"intent\": \"ownership_query\", \"company\": \"Twinize\"}\n"
            "- \"Who does Deepin belong to?\" → {\"intent\": \"ownership_query\", \"company\": \"Deepin\"}\n"
            "- \"What is the authorized signatory of Erdem Ltd?\" → {\"intent\": \"authorization_query\", \"company\": \"Erdem Ltd\"}\n"
            "- \"When was Tayfun's power of attorney valid?\" → {\"intent\": \"authorization_query\", \"company\": null}\n\n"
            f"Question: \"{question}\""
        )
        
        response = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })

        try:
            content = response.json()["response"]
            parsed = json.loads(content.strip())
            return parsed
        except Exception as e:
            print("LLM output parse error:", e)
            print("LLM raw response:", response.text)
            return {"intent": "other", "company": None}