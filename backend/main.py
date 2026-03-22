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

    vulnerable_preview = None
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

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def verify_key(key: str = Security(API_KEY_HEADER)):
    if key != os.getenv("PROMPTSHIELD_API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")