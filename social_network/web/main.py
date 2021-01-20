import os.path
from functools import lru_cache

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from social_network.settings import ROOT_DIR
from social_network.db.excpetions import RowsNotFoundError

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


@app.get('{full_path:path}', response_class=HTMLResponse)
def get_frontend():
    return load_frontend()


@lru_cache(1)
def load_frontend() -> str:
    with open(INDEX) as fp:
        return fp.read()
