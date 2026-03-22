import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class AnalysisResult:
    risk_score: int
    decision: str
    confidence: float
    patterns_detected: list
    attack_types: list
    reason_codes: list
    explanation: str
    recommendation: str
    safe_prompt: str
    rule_hits: list

class PromptShield:
    def __init__(self, api_key: str, base_url: str = "https://promptshield.up.railway.app/"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        })

    def analyze(self, prompt: str) -> AnalysisResult:
        response = self.session.post(
            f"{self.base_url}/analyze",
            json={"prompt": prompt}
        )
        response.raise_for_status()
        data = response.json()["analysis"]
        return AnalysisResult(**data)

    def is_safe(self, prompt: str) -> bool:
        return self.analyze(prompt).decision == "ALLOW"