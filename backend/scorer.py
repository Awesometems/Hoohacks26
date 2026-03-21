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

<<<<<<< Updated upstream
    for pattern_type in patterns_detected:
        if pattern_type == "instruction_override":
            score += 30
        elif pattern_type == "system_prompt_extraction":
            score += 35
        elif pattern_type == "role_hijacking":
            score += 25
        elif pattern_type == "safety_evasion":
            score += 15
        elif pattern_type == "data_exfiltration":
            score += 40
        elif pattern_type == "policy_bypass":
            score += 30
        elif pattern_type == "covert_phrasing":
            score += 20
=======
    categories_seen = set()
>>>>>>> Stashed changes

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