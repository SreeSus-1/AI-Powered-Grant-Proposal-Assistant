from agents.base_agent import BaseAgent

class ReviewerSimulationAgent(BaseAgent):
    def run(self, outline: str, budget: str, funding_agency: str) -> str:
        prompt = f"""
        You are a Reviewer Simulation Agent for grant proposals.

        Review the following proposal draft and budget as if you are evaluating it
        for funding from {funding_agency}.

        Proposal Outline:
        {outline[:3000]}

        Budget:
        {budget[:2000]}

        Provide:
        - strengths
        - weaknesses
        - missing details
        - reviewer concerns
        - improvement suggestions
        - overall funding readiness

        Keep the feedback realistic and constructive.
        """
        return self.call_ollama(prompt)