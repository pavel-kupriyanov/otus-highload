import os.path
from asyncio import get_running_loop
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from social_network.settings import (
    ROOT_DIR,
    settings,
    KafkaSettings,
    MasterSlaveDatabaseSettings
)
from social_network.db.exceptions import RowsNotFoundError
from social_network.db.connectors_storage import ConnectorsStorage
from social_network.services.kafka import (
    KafkaProducer,
    NewsKafkaDatabaseConsumer,
    NewsKafkaCacheConsumer,
    PopulateNewsKafkaConsumer,
    KafkaConsumersManager,
)

from .api import router as api_router

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


async def get_connectors_storage(conf: MasterSlaveDatabaseSettings):
    connectors_storage = ConnectorsStorage()
    await connectors_storage.create_connector(conf.MASTER)

    for conf in conf.SLAVES:
        await connectors_storage.create_connector(conf)

    return connectors_storage


async def get_kafka_producer(conf: KafkaSettings):
    producer = KafkaProducer(conf)
    await producer.start()
    return producer


async def get_news_kafka_consumer_storage(
        conf: KafkaSettings,
        connector_storage: ConnectorsStorage,
        kafka_producer: KafkaProducer
) -> KafkaConsumersManager:
    consumer_classes = [
        NewsKafkaCacheConsumer,
        NewsKafkaDatabaseConsumer,
        PopulateNewsKafkaConsumer
    ]
    consumer_storage = KafkaConsumersManager(
        conf,
        consumer_classes,
        connector_storage,
        kafka_producer,
        get_running_loop()
    )
    await consumer_storage.start()
    return consumer_storage


@app.on_event('startup')
async def startup():
    kafka_conf = settings.KAFKA
    connector_storage = await get_connectors_storage(settings.DATABASE)
    kafka_producer = await get_kafka_producer(kafka_conf)
    app.state.consumers = await get_news_kafka_consumer_storage(
        kafka_conf,
        connector_storage,
        kafka_producer
    )
    app.state.kafka_producer = kafka_producer
    app.state.connectors_storage = connector_storage


@app.on_event('shutdown')
async def shutdown():
    await app.state.kafka_producer.close()
    await app.state.kafka_news_consumer.close()


@app.get('{full_path:path}', response_class=HTMLResponse)
def get_frontend(full_path: str):
    return load_frontend()


@lru_cache(1)
def load_frontend() -> str:
    with open(INDEX) as fp:
        return fp.read()
