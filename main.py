
from reasoner_agent import FinancialTwin


twin = FinancialTwin("ontology/kyc.owl", "ontology/time_reactor.owl")
print(twin.ask("Who are the shareholders of TimeReactorAI?"))