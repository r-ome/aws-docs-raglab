from uuid import uuid4
from datetime import datetime, timezone
from app.ingestion.fetcher import FetchResult

def find_or_create_document(conn, url: str, title: str | None) -> tuple[str, bool]:
    row = conn.execute(
        "SELECT document_id FROM documents WHERE url = ?", [url]
    ).fetchone()
    
    if row:
        return row["document_id"], False
    
    doc_id = str(uuid4())
    conn.execute(
        """
        INSERT INTO documents(document_id, url, title, created_at)
        VALUES(?, ?, ?, ?)
        """,
        [doc_id, url, title, datetime.now(timezone.utc).isoformat()]
    )
    return doc_id, True

def get_latest_content_hash(conn, doc_id) -> str | None:
    row = conn.execute("""
        SELECT content_hash
        FROM document_versions
        WHERE doc_id = ?
        ORDER BY fetched_at desc
        LIMIT 1;
    """, [doc_id]).fetchone()
    return row["content_hash"] if row else None
   
def insert_version(conn, doc_id, fetch_result: FetchResult, content_hash, raw_path, normalized_path, changed_from_previous) -> str:
    version_id = str(uuid4())
    conn.execute("""
        INSERT INTO document_versions(version_id, doc_id, url, fetched_at, http_status, content_hash, raw_path, normalized_path, changed_from_previous)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
    [
        version_id,
        doc_id,
        fetch_result["url"],
        datetime.now(timezone.utc).isoformat(),
        fetch_result["status_code"],
        content_hash,
        raw_path,
        normalized_path,
        changed_from_previous
    ]
    )
    return version_id
