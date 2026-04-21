from uuid import uuid4
from datetime import datetime, timezone
from app.indexing.chunker import chunk_text, estimate_tokens
from app.indexing.embedder import embed_texts
from app.indexing.vector_store import upsert_chunks, delete_by_doc_id

def index_document(conn, doc_id: str, version_id: str, url: str, normalized_text: str):
	print(f"[index] Starting indexing for {url}")

	delete_by_doc_id(doc_id)
	print(f"[index] Cleared old vectors for doc_id={doc_id}")

	chunks = chunk_text(normalized_text)
	print(f"[index] Created {len(chunks)} chunks")

	if not chunks:
		print(f"[index] No chunks to index, skipping")
		return

	texts = [c["text"] for c in chunks]
	embeddings = embed_texts(texts)
	print(f"[index] Generated {len(embeddings)} embeddings")

	chunk_ids = []
	metadatas = []

	for chunk in chunks:
		chunk_id = str(uuid4())
		chunk_ids.append(chunk_id)
		metadatas.append({
			"doc_id": doc_id,
			"version_id": version_id,
			"url": url,
			"chunk_index": chunk["chunk_index"]
		})
		token_est = estimate_tokens(chunk["text"])
		conn.execute("""
			INSERT INTO chunks(chunk_id, doc_id, version_id, chunk_index, text, token_estimate, char_count, vector_store_id, created_at)
			VALUES (?,?,?,?,?,?,?,?,?);
		""", [chunk_id, doc_id, version_id, chunk["chunk_index"], chunk["text"], token_est, len(chunk["text"]), chunk_id, datetime.now(timezone.utc).isoformat()])

	upsert_chunks(chunk_ids, embeddings, texts, metadatas)
	print(f"[index] Upserted {len(chunk_ids)} vectors into Chroma")
	print(f"[index] Done indexing {url}")
