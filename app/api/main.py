from fastapi import FastAPI, APIRouter
from app.db import init_db
from app.api.routes_query import router as query_router
from app.api.routes_health import router as health_router

app = FastAPI()

app.include_router(query_router)
app.include_router(health_router)

@app.on_event("startup")
def startup():
	init_db()
