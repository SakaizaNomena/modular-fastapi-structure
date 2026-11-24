from fastapi import FastAPI
from src.api.routes import api_router
from src.core.config import settings
from contextlib import asynccontextmanager
from src.database.connection import engine
from src.database.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Enregistrement des routes
app.include_router(
    api_router,
    prefix="/api/v1",
)



