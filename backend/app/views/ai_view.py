from fastapi import APIRouter, Body
from ..services.ai_service import ask_gemini

router = APIRouter()

@router.post("/ask-ai")
def ask_ai(question: str = Body(..., embed=True)):
    answer = ask_gemini(question)
    return {"answer": answer}