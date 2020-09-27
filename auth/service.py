import asyncio

from aiohttp import web

from auth import cfg
from auth.rest_api import RestApi


class Service(object):
    __slots__ = ['app', '_rest_api']

    def __init__(self):
        self.app = web.Application()
        self._rest_api = RestApi()
        self.app.router.add_routes([
            web.post(f'{cfg.REST_URL_PREFIX}/login', self._rest_api.login),
            web.get(f'{cfg.REST_URL_PREFIX}/auth', self._rest_api.auth)
        ])
