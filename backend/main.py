from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

@app.post("/secure-query")
def secure_query(request: PromptRequest):
    prompt = (request.prompt or "").strip()
    analysis = analyze_prompt(prompt)

<<<<<<< Updated upstream
    if not prompt:
        return {
            "status": "allowed",
            "decision": "ALLOW",
            "analysis": {
                "risk_score": 0,
                "decision": "ALLOW",
                "patterns_detected": [],
                "attack_types": [],
                "explanation": "Empty prompt — nothing to analyze.",
                "safe_prompt": "",
                "highlighted_attacks": []
            },
            "llm_response": None,
            "vulnerable_preview": None,
        }

=======
    vulnerable_preview = None
>>>>>>> Stashed changes
    if prompt:
        try:
            vulnerable_preview = vulnerable_llm(prompt)
        except Exception:
            vulnerable_preview = "Preview unavailable."

    if analysis["decision"] == "BLOCK":
        return {
            "status": "blocked",
            "analysis": analysis,
            "vulnerable_preview": vulnerable_preview
        }

    return {
        "status": "allowed",
        "analysis": analysis,
        "llm_response": vulnerable_preview,
        "vulnerable_preview": vulnerable_preview
    }