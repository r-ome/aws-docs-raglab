from fastapi import APIRouter
from app.api.schemas import AskRequest
from app.generation.answer_service import ask as ask_question

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/ask")
def ask(request: AskRequest):
	result = ask_question(request.question)
	return result

