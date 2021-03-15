import os.path
from asyncio import get_running_loop, create_task
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from social_network.settings import ROOT_DIR, settings
from social_network.db.exceptions import RowsNotFoundError
from social_network.db.managers import NewsManager
from social_network.services.kafka import KafkaConsumersService

from social_network.services import DependencyInjector
from .api import router as api_router
from .utils import warmup_news

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(ROOT_DIR, 'app/frontend/static')
INDEX = os.path.join(ROOT_DIR, 'app/frontend/index.html')

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.exception_handler(RowsNotFoundError)
async def handle_404(request: Request, exc: RowsNotFoundError):
    return JSONResponse(status_code=404, content={'detail': 'Not found'})


app.include_router(api_router, prefix='/api')


@app.on_event('startup')
async def startup():
    injector = DependencyInjector(settings)
    await injector.start()
    kafka_consumers_service = KafkaConsumersService(
        settings.KAFKA, settings.NEWS_CACHE,
        injector=injector, loop=get_running_loop()
    )
    await kafka_consumers_service.start()
    coro = warmup_news(
        settings.NEWS_CACHE,
        NewsManager(injector.connectors_storage),
        injector.kafka_producer
    )
    create_task(coro)
    app.state.dependency_injector = injector
    app.state.kafka_consumers_service = kafka_consumers_service


@app.on_event('shutdown')
async def shutdown():
    await app.state.dependency_injector.close()
    await app.state.kafka_consumers_service.close()


@app.get('{full_path:path}', response_class=HTMLResponse)
def get_frontend(full_path: str):
    return load_frontend()


@lru_cache(1)
def load_frontend() -> str:
    with open(INDEX) as fp:
        return fp.read()
