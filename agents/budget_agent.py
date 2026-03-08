from agents.base_agent import BaseAgent

class BudgetEstimatorAgent(BaseAgent):
    def run(self, topic: str, goals: str, funding_agency: str) -> str:
        prompt = f"""
        You are a Budget Estimator Agent for grant proposals.

        Generate a realistic draft budget for the following proposal:

        Topic: {topic}
        Goals: {goals}
        Funding Agency: {funding_agency}

        Include estimated categories such as:
        - Personnel
        - Software / Tools
        - Cloud / Infrastructure
        - Data Collection / Materials
        - Travel / Outreach
        - Contingency
        - Total Estimated Budget

        Keep the budget clear and professional.
        """
        return self.call_ollama(prompt)