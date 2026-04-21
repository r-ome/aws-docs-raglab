from pathlib import Path
from app.config import settings 
from app.ingestion.hashing import hash_content

def save_raw_fetch(url:str, content:str) -> str:
	raw_dir = Path(settings.raw_data_dir)
	raw_dir.mkdir(parents=True, exist_ok=True)

	url_hash = hash_content(url)[:12]
	file_path = raw_dir / f"{url_hash}.html"

	file_path.write_text(content, encoding="utf-8")
	return str(file_path)

def save_normalized_document(content: str, url: str) -> str:
	normalized_dir = Path(settings.normalized_data_dir)
	normalized_dir.mkdir(parents=True, exist_ok=True)

	url_hash = hash_content(url)[:12]
	content_hash = hash_content(content)[:12]
	file_path = normalized_dir / f"{url_hash}_{content_hash}.txt"
	file_path.write_text(content, encoding="utf-8")
	return str(file_path)
