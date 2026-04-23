import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, HttpUrl
from pathlib import Path

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env")
	source_config_path: str = "sources/aws_sources.yaml"
	db_path: str = "data/sqlite/raglab.db"
	raw_data_dir: str = "data/raw"
	normalized_data_dir: str = "data/normalized"
	chunk_size: int = 200
	chunk_overlap: int = 50
	embedding_model: str = "all-MiniLM-L6-v2"
	chroma_path: str = "data/chroma"
	top_k: int = 5
	max_distance: float = 1.0
	min_chunks_for_answer: int = 1
	ollama_model: str = "mistral"
	llm_url: str = "http://localhost:11434/api/generate"
	debug: bool = True

class SourceConfig(BaseModel):
	url: HttpUrl
	title: str | None = None
	enabled: bool = True

class SourceFile(BaseModel):
	sources: list[SourceConfig]

settings = Settings()

def load_allowed_sources() -> list[SourceConfig]:
	path = Path(settings.source_config_path)
	if not path.exists():
		raise FileNotFoundError(path)

	data = yaml.safe_load(path.read_text()) or {}
	parsed = SourceFile.model_validate(data)

	allowed: list[SourceConfig] = []
	for source in parsed.sources:
		if source.enabled:
			allowed.append(source)
	return allowed
