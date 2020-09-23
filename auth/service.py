import asyncio

from aiohttp import web

from auth import cfg
from auth.auth_api import AuthApi


class Service(object):
    __slots__ = ['app', '_auth_api']

    def __init__(self):
        self.app = web.Application()
        self._auth_api = AuthApi()
        self.app.router.add_routes(
            [web.post(f'{cfg.REST_URL_PREFIX}/login', self._auth_api.login)])
