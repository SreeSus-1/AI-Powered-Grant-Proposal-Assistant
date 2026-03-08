from agents.base_agent import BaseAgent

class OutlineDesignerAgent(BaseAgent):
    def run(self, topic: str, goals: str, funding_agency: str) -> str:
        prompt = f"""
        You are an Outline Designer Agent for grant proposals.

        Create a structured grant proposal outline for:

        Topic: {topic}
        Goals: {goals}
        Funding Agency: {funding_agency}

        Include:
        - Project Title
        - Executive Summary
        - Problem Statement
        - Objectives
        - Methodology
        - Expected Outcomes
        - Timeline
        - Conclusion

        Keep it professional and funding-oriented.
        """
        return self.call_ollama(prompt)