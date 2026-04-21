import typer
import traceback
from httpx import HTTPError
from sqlite3 import Error as DBError
from app.config import settings
from app.db import init_db
from app.ingestion.fetcher import list_allowed_sources
from app.ingestion.sync import process_source 

app = typer.Typer()

@app.command("init")
def init():
	init_db()
	typer.echo("Database initialized")

@app.command("ask")
def ask(question: str):
	print(question)

@app.command("healthcheck")
def healthcheck():
	typer.echo("OK")

@app.command("show-config")
def show_config():
	"""Show current app config"""
	typer.echo(f"db_path:{settings.db_path}")

@app.command("sources")
def list_docs():
	"""Show allowed list"""
	typer.echo(f"Allowed Sources: {list_allowed_sources()}")

@app.command("sync")
def sync():
	allowed_sources = list_allowed_sources()

	if not allowed_sources:
		typer.echo("No Sources Found")
		return

	results = []
	success = 0
	failed = 0
	
	for source in allowed_sources:
		current = { "status": "", "url": source.url, "ok": False, "error": None}
		
		try:
			result = process_source(source)
			current["ok"] = True
			current["status"] = result["status"]
			success += 1
		except HTTPError as e:
			current["error"] = str(e)
			failed += 1
		except DBError as e:
			current["error"] = str(e)
			failed += 1
		except Exception as e:
			print(traceback.format_exc())
			current["error"] = str(e)
			failed += 1
		results.append(current)

		typer.echo(f"Current: {current['url']}, status: {current['status']}, error: {current['error']}")	

	typer.echo(f"Done. Success: {success} Failed: {failed}")

if __name__ == "__main__":
	app()
