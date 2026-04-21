import chromadb
from app.config import settings

_client = None
_collection = None

def get_collection():
	global _client, _collection
	if _collection is None:
		_client = chromadb.PersistentClient(path=settings.chroma_path)
		_collection = _client.get_or_create_collection(
			name="aws_docs",
			metadata={"hnsw:space": "cosine"}
		)
	return _collection

def upsert_chunks(ids: list[str], embeddings: list[list[float]], documents: list[str], metadatas: list[dict]):
	collection = get_collection()
	collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

def delete_by_doc_id(doc_id: str):
	collection = get_collection()
	collection.delete(where={"doc_id": doc_id})

