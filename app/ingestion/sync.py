from app.config import SourceConfig
from app.db import get_connection
from app.ingestion.fetcher import fetch_source
from app.ingestion.storage import save_raw_fetch, save_normalized_document
from app.ingestion.fetch_repo import find_or_create_document, get_latest_content_hash, insert_version
from app.ingestion.html_parser import parse_html
from app.ingestion.normalizer import normalize_text
from app.ingestion.hashing import hash_content
from app.indexing.index_service import index_document

def process_source(source: SourceConfig):
	fetch_result = fetch_source(source)
	content = str(fetch_result["content"])
	url = str(fetch_result["url"])
	parsed_html = parse_html(content)
	normalized_text = normalize_text(parsed_html["content"])

	conn = get_connection()
	try:
		doc_id, is_new = find_or_create_document(conn, url, parsed_html["title"])
		content_hash = hash_content(normalized_text)
		if not is_new:
			prev_hash = get_latest_content_hash(conn, doc_id)
			if prev_hash == content_hash:
				return { "url": url, "status": "Unchanged"}

		raw_path = save_raw_fetch(url,content)
		normalized_path = save_normalized_document(normalized_text, url)
		status = "New" if is_new else "Changed"
		version_id = insert_version(conn, doc_id, fetch_result, content_hash, raw_path, normalized_path, changed_from_previous=(status != "New"))
		index_document(conn, doc_id, version_id, url, normalized_text)
		conn.commit()
	finally:
		conn.close()	
 
	return { "url": url, "status": status }
