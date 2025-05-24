import requests
import json

class QuestionAnalyzer:
    def __init__(self, llm_url="http://localhost:11434/api/generate", llm_model="mistral"):
        self.llm_url = llm_url
        self.llm_model = llm_model

    def analyze(self, question):
        prompt = f"""
You are an ontology-aware assistant. Given a user question in English, extract the entity and the property involved.

Ontology Summary:
- Classes: Company, RealPerson, Shareholder, Ownership
- Object Properties:
    - hasShareholder: connects Company to Shareholder
    - hasAuthorizedSignatory: connects Company to AuthorizedSignatory
    - hasPowerOfAttorney: connects AuthorizedSignatory to PowerOfAttorney
    - ofAuthorizationType: connects PowerOfAttorney to AuthorizationType
    - representsCompany: connects PowerOfAttorney to Company
- Data Properties:
    - sharePercentage: decimal value representing ownership percentage
    - startDate, endDate: define the validity of a power of attorney

Examples:
Question: Who are the shareholders of TimeReactorAI?
Answer: {{"entity": "TimeReactorAI", "property": "hasShareholder"}}

Question: Who has the authority to sign contracts on behalf of TimeReactorAI?
Answer: {{"entity": "TimeReactorAI", "property": "hasAuthorizedSignatory"}}

Now, answer the following:
Question: {question}
Answer:
"""
        try:
            response = requests.post(
                self.llm_url,
                json={
                    "model": self.llm_model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            result = response.json()
            answer_text = result.get("response", "{}").strip()
            print("[Analyzer] LLM Response:", answer_text)
            return json.loads(answer_text)
        except Exception as e:
            print("[Analyzer] Error:", e)
            return {"entity": None, "property": None}

# Example usage:
# analyzer = QuestionAnalyzer()
# print(analyzer.analyze("Who are the shareholders of TimeReactorAI?"))
