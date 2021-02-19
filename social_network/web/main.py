import os.path
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from social_network.settings import ROOT_DIR, settings
from social_network.db.exceptions import RowsNotFoundError
from social_network.db.connectors_storage import ConnectorsStorage

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


@app.on_event("startup")
async def startup():
    db = settings.DATABASE
    connectors_storage = ConnectorsStorage()
    await connectors_storage.create_connector(db.MASTER)

    for conf in db.SLAVES:
        await connectors_storage.create_connector(conf)

    app.state.connectors_storage = connectors_storage


@app.get('{full_path:path}', response_class=HTMLResponse)
def get_frontend(full_path: str):
    return load_frontend()


@lru_cache(1)
def load_frontend() -> str:
    with open(INDEX) as fp:
        return fp.read()
