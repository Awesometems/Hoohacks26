from patterns import patterns


def find_rule_hits(prompt):
    hits = []
    lowered_prompt = prompt.lower()

    for attack_type, config in patterns.items():
        severity = config["severity"]
        reason_code = config["reason_code"]

        for phrase in config["phrases"]:
            start = lowered_prompt.find(phrase)
            if start != -1:
                original_text = prompt[start:start + len(phrase)]
                hits.append({
                    "attack_type": attack_type,
                    "pattern": original_text,
                    "severity": severity,
                    "reason_code": reason_code
                })

    return hits