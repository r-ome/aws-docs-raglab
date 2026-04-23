import pytest

@pytest.fixture
def sample_chunks():
	return [
	{
		"text": "Amazon Bedrock is a fully managed service for foundation models.",
		"metadata": {
			"url": "https://docs.aws.amazon.com/bedrock",
			"title": "Bedrock Overview",
			"doc_id": "doc_1",
		},
		"distance": 0.3,
		"rank": 1,
		"source_url": "https://docs.aws.amazon.com/bedrock",
		"doc_id": "doc_1",
		"version_id": "v1",
		"chunk_index": 0,
	},
	{
		"text": "You can invoke models using the InvokeModel API",
		"metadata": {
			"url": "https://docs.aws.amazon.com/bedrock/api",
			"title": "Bedrock API",
			"doc_id": "doc_2"
		},
		"distance": 0.5,
		"rank": 2,
		"source_url": "https://docs.aws.amazon.com/bedrock/api",
		"doc_id": "doc_2",
		"version_id": "v2",
		"chunk_index": 1
	}
	]
