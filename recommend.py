import json

with open("cards.json") as f:
    cards = json.load(f)

# Map credit score descriptions to numeric values
credit_score_map = {
    "poor": 600,
    "average": 650,
    "good": 700,
    "unknown": 0
}

def recommend_cards(user):
    try:
        income = int(user.get("income", 0))
    except:
        income = 0

    spending = user.get("spending", "").lower()
    benefits = user.get("benefits", "").lower()
    credit_score = credit_score_map.get(user.get("credit_score", "unknown").lower(), 0)

    matched_cards = []

    for card in cards:
        min_income = card.get("eligibility", {}).get("min_income", 0)
        min_score = card.get("eligibility", {}).get("credit_score", 0)
        categories = [c.lower() for c in card.get("categories", [])]

        # Basic eligibility match
        if income >= min_income and (credit_score == 0 or credit_score >= min_score):
            # Check preference alignment
            if any(b in categories for b in benefits.split(',')) or \
               any(s in categories for s in spending.split(',')):
                matched_cards.append(card)

    # Fallback logic if fewer than 3
    if len(matched_cards) < 3:
        remaining = [c for c in cards if c not in matched_cards]
        matched_cards.extend(remaining[:3 - len(matched_cards)])

    return matched_cards[:3]
