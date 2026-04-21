from fastapi import APIRouter
from app.api.schemas import AskRequest

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/ask")
def ask(request: AskRequest):
	print(request)
	return { "question": request.question }
