from patterns import patterns

# Severity and reason codes per category (mirrors analyzer.py PATTERN_META)
PATTERN_META = {
    "instruction_override":     {"severity": 40, "reason_code": "INSTR_OVERRIDE"},
    "role_manipulation":        {"severity": 35, "reason_code": "ROLE_MANIP"},
    "data_exfiltration":        {"severity": 45, "reason_code": "DATA_EXFIL"},
    "safety_bypass":            {"severity": 25, "reason_code": "SAFETY_BYPASS"},
    "jailbreak":                {"severity": 40, "reason_code": "JAILBREAK"},
}


def find_rule_hits(prompt):
    hits = []
    lowered = prompt.lower()

    for attack_type, phrases in patterns.items():
        meta = PATTERN_META.get(attack_type, {"severity": 10, "reason_code": "UNKNOWN"})
        for phrase in phrases:
            start = lowered.find(phrase)
            if start != -1:
                hits.append({
                    "attack_type": attack_type,
                    "pattern":     prompt[start:start + len(phrase)],
                    "severity":    meta["severity"],
                    "reason_code": meta["reason_code"],
                })

    return hits