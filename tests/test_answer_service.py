from unittest.mock import patch
from app.generation.answer_service import ask

@patch("app.generation.answer_service.retrieve", return_value =[])
def test_ask_no_chunks(mock_retrieve):
	result = ask("anything")
	assert "don't have enough information" in result["answer"]
	assert result["chunks_used"] == 0

@patch("app.generation.answer_service.generate", side_effect=Exception("connection refused"))
@patch("app.generation.answer_service.retrieve")
def test_ask_ollama_failure(mock_retrieve, mock_generate, sample_chunks):
	mock_retrieve.return_value = sample_chunks
	result = ask("What is Bedrock?")
	assert "Generation Failed" in result["answer"]

@patch("app.generation.answer_service.generate", return_value="Bedrock is a managed service[1].")
@patch("app.generation.answer_service.retrieve")
def test_ask_returns_sources(mock_retrieve, mock_generate, sample_chunks):
	mock_retrieve.return_value = sample_chunks
	result = ask("What is Bedrock?")
	assert result["chunks_used"] == 2
	assert len(result["sources"]) > 0
	assert result["sources"][0]["url"] == "https://docs.aws.amazon.com/bedrock"
