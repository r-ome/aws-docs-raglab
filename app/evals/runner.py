import json
from pathlib import Path
from app.generation.answer_service import ask

def run_eval(dataset_path: str, output_path: str):
	results = []
	with open(dataset_path) as f:
		questions = [json.loads(line) for line in f if line.strip()]

	for q in questions:
		response = ask(q["question"])
		result = {
			"id": q["id"],
			"question": q["question"],
			"category": q["category"],
			"answer": response["answer"],
			"sources": response["sources"],
			"chunks_used": response["chunks_used"],
			"expected_source_urls": q.get("expected_source_urls", []),
			"expected_keywords": q.get("expected_keywords", []),
		}
		results.append(result)

	Path(output_path).parent.mkdir(parents=True, exist_ok=True)
	with open(output_path, "w") as f:
		for r in results:
			f.write(json.dumps(r) + "\n")

	return results
