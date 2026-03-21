from patterns import patterns


def highlight_prompt(prompt):
    findings = []
    lowered_prompt = prompt.lower()

    for category, rules in patterns.items():
        for rule in rules:
            start = lowered_prompt.find(rule)
            if start != -1:
                original_text = prompt[start:start + len(rule)]
                findings.append({
                    "pattern": original_text,
                    "attack_type": category
                })

    return findings