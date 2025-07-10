"""
api_service.py
Start with:  uvicorn api_service:app --reload
Browse at:   http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel
from generator import generate_password, score_password, hibp_pwned

app = FastAPI(
    title="Password‑Smith API",
    description="Generate and analyse passwords. See /docs for Swagger UI.",
    version="1.0.0",
)

# ---------- pydantic models ---------- #
class PwOut(BaseModel):
    password: str
    strength: int
    pwned: bool
    pwned_count: int


class PwIn(BaseModel):
    password: str


# ---------- friendly root route ---------- #
@app.get("/")
def root():
    return {
        "message": "Welcome to Password‑Smith API 🎉",
        "docs": "/docs",
        "endpoints": ["/generate (GET)", "/analyze (POST)"],
    }


# ---------- /generate ---------- #
@app.get("/generate", response_model=PwOut, summary="Generate a strong password")
def api_generate(
    length: int = Query(16, ge=8, le=64),
    digits: bool = True,
    symbols: bool = True,
    uppercase: bool = True,
    lowercase: bool = True,
):
    pwd = generate_password(
        length=length,
        digits=digits,
        symbols=symbols,
        uppercase=uppercase,
        lowercase=lowercase,
    )
    leaks = hibp_pwned(pwd)
    info = score_password(pwd)
    return PwOut(
        password=pwd,
        strength=info["score"],
        pwned=bool(leaks),
        pwned_count=leaks,
    )


# ---------- /analyze ---------- #
@app.post("/analyze", response_model=PwOut, summary="Analyse an existing password")
def api_analyze(body: PwIn):
    leaks = hibp_pwned(body.password)
    info = score_password(body.password)
    return PwOut(
        password=body.password,
        strength=info["score"],
        pwned=bool(leaks),
        pwned_count=leaks,
    )
