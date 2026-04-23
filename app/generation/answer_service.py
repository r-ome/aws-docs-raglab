from app.retrieval.retriever import retrieve
from app.retrieval.context_builder import build_context, build_prompt
from app.generation.llm_client import generate
from app.config import settings

def ask(question: str) -> dict:
	chunks = retrieve(question)

	if not chunks or len(chunks) < settings.min_chunks_for_answer:
		return {
			"answer": "I don't have enough information to answer this question.",
			"sources": [],
			"chunks_used": len(chunks),
		}

	context = build_context(chunks)
	prompt = build_prompt(question, context)

	try:
		answer = generate(prompt)
	except Exception as e:
		return {
			"answer": f"Generation Failed: {e}",
			"sources": [],
			"chunks_used": 0
		}

	sources = []
	seen = set()
	for i, chunk in enumerate(chunks, start=1):
		metadata = chunk["metadata"] or {}
		url = metadata.get("url", "")
		title = metadata.get("title", "")
		if url not in seen:
			sources.append({ "ref": i, "url": url, "title": title })
			seen.add(url)

	result = {
		"answer": answer,
		"sources": sources,
		"chunks_used": len(chunks),
	}

	if settings.debug:
		result["debug"] = {
			"retrieved_chunks": [
				{
					"rank": c["rank"],
					"distance": c["distance"],
					"doc_id": c["doc_id"],
					"source_url": c["source_url"],
					"text_preview": c["text"][:100],
				}
			for c in chunks
			],
			"prompt_length": len(prompt)

		}
	return result
