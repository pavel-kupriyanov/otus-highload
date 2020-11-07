import uvicorn


def run():
    uvicorn.run('web:app', host='0.0.0.0', port=8000, reload=True)
