def build_context(chunks: list[dict]) -> str:
	if not chunks:
		return ""

	context_parts = []
	for i, chunk in enumerate(chunks, start=1):
		metadata = chunk["metadata"] or {}
		url = metadata.get("url", "unknown")
		context_parts.append(f"[{i}] Source: {url}\n{chunk['text']}")

	return "\n\n---\n\n".join(context_parts)

def build_prompt(question: str, context: str) -> str:
	return f"""You are an AWS documentation assistant. Answer the question using ONLY the provided context. Do not invent facts.

	If the context does not contain enough information to answer, say: "I don't have enough information to answer this question."

	Cite your sources using the reference numbers (e.g., [1], [2]).

	Context:
	{context}

	Question: {question}

	Answer:"""
