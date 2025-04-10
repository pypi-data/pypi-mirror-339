import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from src.app.config.logger import logger
from src.app.config.settings import settings
from src.app.models import init_models
from src.app.routes import get_registered_routes
from src.app.routes.cards import router as cards_router
from src.app.routes.mtgo import router as mtgo_router
from src.app.routes.statistics import router as statistics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    print("\n".join(get_registered_routes(app)))
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"Route: {request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )
    return response


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs", status_code=301)


# Inclure les routes
app.include_router(cards_router, prefix="/api/v1", tags=["Cards"])
app.include_router(mtgo_router, prefix="/api/v1", tags=["MTGO"])
app.include_router(statistics_router, prefix="/api/v1", tags=["Statistics"])
