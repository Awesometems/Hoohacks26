from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from analyzer import analyze_prompt
from simulator import vulnerable_llm
from config import MODEL_NAME, FALLBACK_MODE

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
        "model": MODEL_NAME if not FALLBACK_MODE else "fallback-mode",
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
    decision = analysis["decision"]

    vulnerable_response = None
    if prompt:
        try:
            vulnerable_response = vulnerable_llm(prompt)
        except Exception:
            vulnerable_response = "Vulnerable model response unavailable."

    is_safe = decision == "ALLOW" and analysis["risk_score"] == 0

    return {
        "status": "blocked" if decision == "BLOCK" else "allowed",
        "safe": is_safe,
        "safety_message": "✅ Prompt is clean — no threats detected." if is_safe else None,
        "decision": decision,
        "analysis": analysis,
        "llm_response": None if decision == "BLOCK" else vulnerable_response,
        "vulnerable_preview": vulnerable_response,
    }