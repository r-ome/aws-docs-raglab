from app.config import settings

def estimate_tokens(text: str) -> int:
	return len(text.split())

def chunk_text(text: str, chunk_size: int = settings.chunk_size, chunk_overlap: int = settings.chunk_overlap) -> list[dict]:
	paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
	chunks = []
	current_paragraphs = []
	current_tokens = 0

	for para in paragraphs:
		para_tokens = estimate_tokens(para)

		if current_tokens + para_tokens > chunk_size and current_paragraphs:
			chunk_text_str = "\n\n".join(current_paragraphs)
			chunks.append({ "chunk_index": len(chunks), "text": chunk_text_str})

			overlap_paragraphs = []
			overlap_tokens = 0
			for p in reversed(current_paragraphs):
				p_tokens = estimate_tokens(p)
				if overlap_tokens + p_tokens > chunk_overlap:
					break
				overlap_paragraphs.insert(0,p)
				overlap_tokens += p_tokens

			current_paragraphs = overlap_paragraphs
			current_tokens = overlap_tokens

		current_paragraphs.append(para)
		current_tokens += para_tokens

	if current_paragraphs:
		chunk_text_str = "\n\n".join(current_paragraphs)
		chunks.append({ "chunk_index": len(chunks), "text": chunk_text_str })

	return chunks
