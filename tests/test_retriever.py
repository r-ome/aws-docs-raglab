from unittest.mock import patch, MagicMock
from app.retrieval.retriever import retrieve

@patch("app.retrieval.retriever.get_collection")
@patch("app.retrieval.retriever.embed_texts")
def test_retrieve_empty_collection(mock_embed, mock_get_col):
	mock_collection = MagicMock()
	mock_collection.count.return_value = 0
	mock_get_col.return_value = mock_collection
	assert retrieve("anything") == []
	mock_embed.assert_not_called()

@patch("app.retrieval.retriever.get_collection")
@patch("app.retrieval.retriever.embed_texts")
def test_retrieve_filters_by_distance(mock_embed, mock_get_col):
	mock_embed.return_value = [[0.1] * 384]
	mock_collection = MagicMock()
	mock_collection.count.return_value = 2
	mock_collection.query.return_value = {
		"documents": [["good chunk", "bad_chunk"]],
		"metadatas": [[{"url": "a"}, {"url": "b"}]],
		"distances": [[0.3, 1.5]],
	}
	mock_get_col.return_value = mock_collection
	results = retrieve("test query")
	assert len(results) == 1
	assert results[0]["text"] == "good chunk"
