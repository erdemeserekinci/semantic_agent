from owlready2 import get_ontology
from collections import defaultdict

class FinancialTwinAgent:
    def __init__(self, ontology_path):
        self.onto = get_ontology(ontology_path).load()
        self.results = defaultdict(float)

    def trace_ownership(self, company, multiplier=1.0):
        for ownership in company.hasOwnership:
            shareholder = ownership.hasShareholder[0]
            share = float(ownership.sharePercentage[0])
            effective_share = multiplier * share

            if "Person" in shareholder.is_a[0].name:
                name = self.get_label(shareholder)
                self.results[name] += effective_share
            else:
                self.trace_ownership(shareholder, effective_share)

    def get_label(self, individual):
        return individual.firstName[0] if hasattr(individual, "firstName") else individual.name

    def run(self, target_company_name):
        company = self.onto.search_one(legalName=target_company_name)
        if company:
            self.trace_ownership(company)
            return sorted(self.results.items(), key=lambda x: -x[1])
        else:
            return []

# Kullanım:
agent = FinancialTwinAgent("twinize_group_abox.owl")
results = agent.run("Twinize")
for person, share in results:
    print(f"{person}: {share:.2f}%")