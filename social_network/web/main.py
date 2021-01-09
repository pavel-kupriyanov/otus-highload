from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from social_network.db import RowsNotFoundError

from .api import router as api_router

app = FastAPI()


@app.exception_handler(RowsNotFoundError)
async def handle_404(request: Request, exc: RowsNotFoundError):
    return JSONResponse(status_code=404, content={'detail': 'Not found'})


app.include_router(api_router, prefix='/api')
