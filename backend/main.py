from fastapi import FastAPI
from pydantic import BaseModel

from analyzer import analyze_prompt
from simulator import vulnerable_llm

app = FastAPI(title="PromptShield AI Firewall")


class PromptRequest(BaseModel):
    prompt: str


import time
from datetime import datetime

START_TIME = time.time()

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model": "gpt-4o-mini",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/secure-query")
def secure_query(request: PromptRequest):
    prompt = (request.prompt or "").strip()

    analysis = analyze_prompt(prompt)
    decision = analysis["decision"]

    vulnerable_response = None

    if prompt:
        try:
            vulnerable_response = vulnerable_llm(prompt)
        except Exception:
            vulnerable_response = "Vulnerable model response unavailable."

    if decision == "BLOCK":
        return {
            "status": "blocked",
            "analysis": analysis,
            "vulnerable_preview": vulnerable_response
        }

    return {
        "status": "allowed",
        "analysis": analysis,
        "llm_response": vulnerable_response,
        "vulnerable_preview": vulnerable_response
    }