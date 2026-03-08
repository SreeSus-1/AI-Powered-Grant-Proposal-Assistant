import streamlit as st
import pandas as pd

from agents.outline_agent import OutlineDesignerAgent
from agents.budget_agent import BudgetEstimatorAgent
from agents.reviewer_agent import ReviewerSimulationAgent
from memory.proposal_db import save_proposal, get_all_proposals

st.set_page_config(page_title="AI-Powered Grant Proposal Assistant", layout="wide")

outline_agent = OutlineDesignerAgent()
budget_agent = BudgetEstimatorAgent()
reviewer_agent = ReviewerSimulationAgent()

st.title("AI-Powered Grant Proposal Assistant")
st.subheader("Multi-Agent Proposal Drafting Workspace")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Draft Proposal", "Proposal Versions", "About"]
)

if menu == "Draft Proposal":
    st.header("Enter Proposal Details")

    topic = st.text_input("Proposal Topic", "AI-Powered Learning Support for Rural Students")
    goals = st.text_area(
        "Project Goals",
        "Improve access to personalized learning tools, provide AI tutoring support, and measure student engagement outcomes."
    )
    funding_agency = st.text_input("Funding Agency", "National Science Foundation")
    rationale = st.text_area("Version Rationale / Notes", "Initial concept draft")

    if st.button("Generate Proposal Draft"):
        with st.spinner("Designing proposal outline..."):
            outline = outline_agent.run(topic, goals, funding_agency)

        if outline.startswith("ERROR:"):
            st.error(f"Outline Designer failed: {outline}")
        else:
            with st.spinner("Estimating budget..."):
                budget = budget_agent.run(topic, goals, funding_agency)

            if budget.startswith("ERROR:"):
                st.warning("Outline generated successfully, but Budget Estimator timed out.")
                st.subheader("Proposal Outline")
                st.write(outline)
            else:
                with st.spinner("Running reviewer simulation..."):
                    review = reviewer_agent.run(outline, budget, funding_agency)

                if review.startswith("ERROR:"):
                    st.warning("Outline and budget generated, but Reviewer Simulation timed out.")
                    st.subheader("Proposal Outline")
                    st.write(outline)
                    st.subheader("Draft Budget")
                    st.write(budget)
                else:
                    save_proposal(topic, goals, funding_agency, outline, budget, review, rationale)

                    st.success("Proposal draft generated and saved.")

                    st.subheader("Proposal Outline")
                    st.write(outline)

                    st.subheader("Draft Budget")
                    st.write(budget)

                    st.subheader("Reviewer Feedback")
                    st.write(review)

elif menu == "Proposal Versions":
    st.header("Saved Proposal Versions")

    proposals = get_all_proposals()

    if proposals:
        df = pd.DataFrame(proposals)
        st.dataframe(
            df[["timestamp", "version", "topic", "funding_agency"]],
            use_container_width=True
        )

        selected_index = st.number_input(
            "Select proposal index",
            min_value=0,
            max_value=len(proposals) - 1,
            step=1
        )

        proposal = proposals[selected_index]

        st.subheader(f"Topic: {proposal['topic']}")
        st.write(f"Funding Agency: {proposal['funding_agency']}")
        st.write(f"Version: {proposal['version']}")
        st.write(f"Saved on: {proposal['timestamp']}")
        st.write(f"Rationale: {proposal['rationale']}")

        st.markdown("### Proposal Outline")
        st.write(proposal["outline"])

        st.markdown("### Draft Budget")
        st.write(proposal["budget"])

        st.markdown("### Reviewer Feedback")
        st.write(proposal["review"])
    else:
        st.info("No saved proposal versions found yet.")

else:
    st.header("About")
    st.markdown("""
This application helps researchers and nonprofits draft grant proposals using three specialized AI agents:
- Outline Designer
- Budget Estimator
- Reviewer Simulation Agent

It also stores proposal versions and rationale so users can track how drafts evolve over time.
""")