def calculate_risk(patterns_detected, llm_score):
    try:
        score = int(llm_score)
    except (TypeError, ValueError):
        score = 50

    score = max(0, min(score, 100))

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

    score += len(patterns_detected) * 5
    return min(score, 100)