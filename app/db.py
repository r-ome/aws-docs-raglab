from app.config import settings
from pathlib import Path
import sqlite3

def get_connection():
	try:
		conn = sqlite3.connect(settings.db_path)
		conn.row_factory = sqlite3.Row
		return conn
	except sqlite3.Error as e:
		print(f"Database connection failed: {e}")
		raise RuntimeError(f"Database connection failed: {e}") from e

def init_db():
	db_path = Path(settings.db_path)
	db_path.parent.mkdir(parents=True, exist_ok=True)
	conn = get_connection()
 
	conn.execute("PRAGMA foreign_keys = ON")
	conn.execute("""
		CREATE TABLE IF NOT EXISTS schema_migrations(
			versions TEXT PRIMARY KEY,
			applied_at TEXT NOT NULL
		)
	""")
	conn.execute("""
		CREATE TABLE IF NOT EXISTS documents (
			document_id TEXT PRIMARY KEY,
			url TEXT NOT NULL,
			title TEXT,
			category TEXT,
			enabled TEXT,
			created_at TEXT NOT NULL
		)
	""")
	conn.execute("""
		CREATE TABLE IF NOT EXISTS document_versions(
			version_id TEXT PRIMARY KEY,
			doc_id TEXT NOT NULL,
			url TEXT NOT NULL,
			fetched_at TEXT NOT NULL,
			http_status INTEGER NOT NULL,
			content_hash TEXT,
			raw_path TEXT,
			normalized_path TEXT,
			changed_from_previous INTEGER NOT NULL DEFAULT 1,
			FOREIGN KEY (doc_id) REFERENCES documents(document_id)
		)
	""")

	conn.execute("""
		CREATE TABLE IF NOT EXISTS chunks(
			chunk_id TEXT PRIMARY KEY,
			doc_id TEXT NOT NULL,
			version_id TEXT NOT NULL,
			chunk_index INTEGER NOT NULL,
			text TEXT NOT NULL,
			token_estimate INTEGER,
			char_count INTEGER,
			metadata_json TEXT,
			vector_store_id TEXT,
			created_at TEXT NOT NULL,
			FOREIGN KEY (doc_id) REFERENCES documents(document_id),
			FOREIGN KEY (version_id) REFERENCES document_versions(version_id)
		)
	""")
	conn.commit()
	conn.close()
	return "Database initialized"
