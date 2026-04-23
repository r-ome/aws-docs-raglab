from app.retrieval.context_builder import build_context, build_prompt

def test_build_context_empty():
	assert build_context([]) == ""

def test_build_context_includes_refs_and_urls(sample_chunks):
	context = build_context(sample_chunks)
	assert "[1]" in context
	assert "[2]" in context
	assert "https://docs.aws.amazon.com/bedrock" in context
	assert "Amazon Bedrock is a fully managed" in context

def test_build_context_includes_title(sample_chunks):
	context = build_context(sample_chunks)
	assert "Bedrock Overview" in context

def test_build_prompt_contains_question():
	prompt = build_prompt("What is Bedrock?", "some context")
	assert "What is Bedrock?" in prompt
	assert "some context" in prompt
	assert "ONLY the provided context" in prompt
