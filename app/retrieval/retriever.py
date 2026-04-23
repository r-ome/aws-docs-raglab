from app.indexing.embedder import embed_texts
from app.indexing.vector_store import get_collection
from app.config import settings

def retrieve(query: str, top_k: int = settings.top_k) -> list[dict]:
	collection = get_collection()
	count = collection.count()
 
	if count == 0:
		return []

	n_results = min(top_k, count)
	if n_results <= 0:
		return []


	query_embedding = embed_texts([query])[0]
	results = collection.query(
		query_embeddings=[query_embedding],
		n_results=n_results,
		include=["documents", "metadatas", "distances"]
	)
 
	documents = results.get("documents") or []
	metadatas = results.get("metadatas") or []
	distances = results.get("distances") or []

	if not documents or not documents[0]:
		return []

	doc_list = documents[0]
	metadata_list = metadatas[0] if metadatas and metadatas[0] else []
	distance_list = distances[0] if distances and distances[0] else []

	chunks = []
	for i, text in enumerate(doc_list):
		if not text or not text.strip():
			continue

		metadata = {}
		if i < len(metadata_list) and isinstance(metadata_list[i], dict):
			metadata = metadata_list[i]

		distance = None
		if i < len(distance_list):
			distance = distance_list[i]

		chunks.append({
			"text": text,
			"metadata": metadata,
			"distance": distance,
			"rank": i + 1,
			"source_url": metadata.get("url"),
			"doc_id": metadata.get("doc_id"),
			"version_id": metadata.get("version_id"),
			"chunk_index": metadata.get("chunk_index")
		})

	chunks = [
		c for c in chunks
		if c["distance"] is None or c["distance"] <= settings.max_distance
	]
	return chunks
