def score_result(result: dict) -> dict:
	scores = {}

	# Source hit: did any expected URL appear in returned sources?
	returned_urls = [s["url"] for s in result["sources"]] if result["sources"] else []
	expected_urls = result.get("expected_source_urls", [])
	if expected_urls:
		hits = sum(1 for u in expected_urls if any(u in r for r in returned_urls))
		scores["source_hit"] = hits / len(expected_urls)
	else:
		scores["source_hit"] = None

	# Keyword coverage: how many expected keywords appear in the answer?
	expected_kw = result.get("expected_keywords", [])
	if expected_kw:
		answer_lower = result["answer"].lower()
		hits = sum(1 for kw in expected_kw if kw.lower() in answer_lower)
		scores["keyword_coverage"] = hits / len(expected_kw)
	else:
		scores["keyword_coverage"] = None

	# Abstention: for out_of_scope, did the model decline?
	if result["category"] == "out_of_scope":
		scores["abstention_correct"] = "don't have enough information" in result["answer"].lower()
	else:
		scores["abstention_correct"] = None

	# Citation present?
	scores["has_citations"] = bool("[1]" in result["answer"] or "[2]" in result["answer"])

	return scores
