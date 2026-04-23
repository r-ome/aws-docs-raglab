def print_report(results: list[dict], scores: list[dict]):
	total = len(results)
	by_category = {}

	for r, s in zip(results, scores):
		cat = r["category"]
		by_category.setdefault(cat, []).append(s)

	print(f"\nEval Report - {total} questions\n")

	for cat, cat_scores in by_category.items():
		print(f" {cat} ({len(cat_scores)} questions): ")

		src_hits = [s.get("source_hit") for s in cat_scores if s.get("source_hit") is not None]
		if src_hits:
			print(f" source hit rate: {sum(src_hits)/len(src_hits):.0%}")

		kw_hits = [s.get("keyword_coverage") for s in cat_scores if s.get("keyword_coverage") is not None]
		if kw_hits:
			print(f" keyword coverage: {sum(kw_hits)/len(kw_hits):.0%}")

		citations = [s.get("has_citations", False) for s in cat_scores]
		print(f" has citations: {sum(citations)/len(citations)}")

		abstentions = [s.get("abstention_correct") for s in cat_scores if s.get("abstention_correct") is not None]
		if abstentions:
			print(f" abstention correct: {sum(abstentions)}/{len(abstentions)}")

		print()
