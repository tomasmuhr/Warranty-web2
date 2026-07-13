from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import database_ops, items, search, shops, stats


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.db_dir.mkdir(parents=True, exist_ok=True)
    if not settings.database_path.exists():
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Warranty API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router, prefix="/api")
app.include_router(shops.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(database_ops.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "database": str(Path(settings.database_path))}
