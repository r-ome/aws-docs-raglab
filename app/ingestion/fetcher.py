import httpx
from typing import TypedDict
from app.config import load_allowed_sources, SourceConfig

def list_allowed_sources() -> list[SourceConfig]:
	return load_allowed_sources()

class FetchResult(TypedDict):
    url: str
    status_code: int
    content: str
    normalized_text: str

def fetch_source(source: SourceConfig) -> FetchResult:
	url = str(source.url)
	response = httpx.get(url, timeout=30.0)
	response.raise_for_status()
	return { "url": url, "status_code": response.status_code, "content": response.text, "normalized_text":"" }
