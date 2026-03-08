from tinydb import TinyDB
from datetime import datetime

db = TinyDB("proposal_memory.json")

def save_proposal(topic, goals, funding_agency, outline, budget, review, rationale="Initial draft"):
    versions = db.search(lambda x: x.get("topic") == topic and x.get("funding_agency") == funding_agency)
    version_number = len(versions) + 1

    db.insert({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": version_number,
        "topic": topic,
        "goals": goals,
        "funding_agency": funding_agency,
        "outline": outline,
        "budget": budget,
        "review": review,
        "rationale": rationale
    })

def get_all_proposals():
    return db.all()