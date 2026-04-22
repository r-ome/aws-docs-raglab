from app.retrieval.retriever import retrieve
from app.retrieval.context_builder import build_context, build_prompt
from app.generation.llm_client import generate

def ask(question: str) -> dict:
	chunks = retrieve(question)

	if not chunks:
		return {
			"answer": "I don't have enough information to answer this question.",
			"sources": [],
			"chunks_used": 0
		}

	context = build_context(chunks)
	prompt = build_prompt(question, context)
	answer = generate(prompt)

	sources = []
	seen = set()
	for chunk in chunks:
		metadata = chunk["metadata"] or {}
		url = metadata.get("url", "")
		if url not in seen:
			sources.append(url)
			seen.add(url)

	return {
		"answer": answer,
		"sources": sources,
		"chunks_used": len(chunks),
	}
