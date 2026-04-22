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

	chunks = []
	for i, text in enumerate(documents[0]):
		metadata = {}
		if metadatas and metadatas[0] and i < len(metadatas[0]) and metadatas[0][i] is not None:
			metadata = metadatas[0][i]

		distance = None
		if distances and distances[0] and i < len(distances[0]):
			distance = distances[0][i]

		chunks.append({
			"text": text,
			"metadata": metadata,
			"distance": distance,
		})

	return chunks
