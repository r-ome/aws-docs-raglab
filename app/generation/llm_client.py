import httpx
from app.config import settings

def generate(prompt: str) -> str:
	response = httpx.post(
		settings.llm_url,
		json={
			"model": settings.ollama_model,
			"prompt": prompt,
			"stream": False
		},
		timeout=120.0
	)
	response.raise_for_status()
	return response.json()["response"]
