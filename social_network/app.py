import uvicorn

from social_network.settings import UvicornSettings


def run(conf: UvicornSettings, reload=False):
    uvicorn.run(conf.ASGI_PATH, host=conf.HOST, port=conf.PORT, reload=reload)
