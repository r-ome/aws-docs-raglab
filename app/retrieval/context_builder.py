from textwrap import dedent

def build_context(chunks: list[dict]) -> str:
	if not chunks:
		return ""

	context_parts = []
	for i, chunk in enumerate(chunks, start=1):
		metadata = chunk["metadata"] or {}
		title = metadata.get("title", "")
		url = metadata.get("url", "unknown")
		header = f"[{i}] Source: {url}"
		if title:
			header = f"[{i}] {title} - {url}"
		context_parts.append(f"{header}\n{chunk['text']}")

	return "\n\n---\n\n".join(context_parts)

def build_prompt(question: str, context: str) -> str:
	return dedent(f"""
	You are an AWS documentation assistant. Answer the question using ONLY the provided context.
	Do not invent facts.

	If the context does not contain enough information to fully answer the question, say
	exactly:
	"I don't have enough information to answer this question."
	Do NOT attempt a partial or speculative answer. If unsure, abstain.

	Cite your sources using the reference numbers (e.g., [1], [2]).

	Context:
	{context}

	Question: {question}

	Answer:
	""").strip()
