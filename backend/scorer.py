def calculate_risk(rule_hits, llm_score, llm_confidence):
    try:
        score = int(llm_score)
    except (TypeError, ValueError):
        score = 45

    try:
        confidence = float(llm_confidence)
    except (TypeError, ValueError):
        confidence = 0.5

    score = max(0, min(score, 100))
    confidence = max(0.0, min(confidence, 1.0))

    categories_seen = set()

    for hit in rule_hits:
        score += hit["severity"]
        categories_seen.add(hit["attack_type"])

    if len(categories_seen) >= 2:
        score += 8

    if len(categories_seen) >= 3:
        score += 10

    score += int(confidence * 10)

    return min(score, 100)


def firewall_decision(score):
    if score >= 80:
        return "BLOCK"
    if score >= 50:
        return "WARN"
    return "ALLOW"