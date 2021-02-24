import asyncio
import json
import unittest

import aiohttp
from aiohttp import StreamReader, web
from auth import cfg
from auth.service import Service


class TestRest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._host = '127.0.0.1'
        cls._port = 8080
        cls._url = f'http://{cls._host}:{cls._port}/api/v1'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self._service = Service()
        self._loop = asyncio.get_event_loop_policy().new_event_loop()
        self._server = self._loop.run_until_complete(
            self._get_server(self._loop))

    def tearDown(self):
        self._server.close()
        self._loop.run_until_complete(self._server.wait_closed())
        self._loop.run_until_complete(self._service.app.shutdown())
        self._loop.run_until_complete(self._service.app.cleanup())
        self._loop.close()
        del self._service
        del self._loop

    async def _get_server(self, event_loop):
        async def _get_runner():
            runner = web.AppRunner(self._service.app)
            await runner.setup()
            return runner

        runner = await _get_runner()
        server = await event_loop.create_server(runner.server, self._host,
                                                self._port)
        return server

    def _exec_with_server(self, cb):
        coro = asyncio.coroutine(cb)
        self._loop.run_until_complete(coro())

    def test_auth_invalid(self):
        url_auth = f'{self._url}/auth'

        async def helper():
            async with aiohttp.ClientSession() as sess:
                # no token
                async with sess.get(url_auth) as resp:
                    self.assertEquals(401, resp.status)
                # fake token
                fake_token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                              'eyJpc3MiOiJ0b3B0YWwuY29tIiwiZXhwIjoxN'
                              'DI2NDIwODAwLCJodHRwOi8vdG9wdGFsLmNvbS'
                              '9qd3RfY2xhaW1zL2lzX2FkbWluIjp0cnVlLCJ'
                              'jb21wYW55IjoiVG9wdGFsIiwiYXdlc29tZSI6'
                              'dHJ1ZX0.yRQYnWzskCZUxPwaQupWkiUzKELZ4'
                              '9eM7oWxAQK_ZXw')
                async with sess.get(url_auth, headers={'token':
                                                       fake_token}) as resp:
                    self.assertEquals(401, resp.status)

        return self._exec_with_server(helper)

    def test_login_auth(self):
        async def helper():
            async with aiohttp.ClientSession() as sess:
                url_login = f'{self._url}/login'
                url_auth = f'{self._url}/auth'
                data = {
                    'user': cfg.LDAP3_BIND_USR,
                    'password': cfg.LDAP3_BIND_PWD
                }
                async with sess.post(url_login, data=data) as resp:
                    sr: StreamReader = resp.content
                    payload: bytes = await sr.read()
                    token = json.loads(payload.decode()).get('token')
                async with sess.get(url_auth, headers={'token':
                                                       token}) as resp:
                    self.assertEquals(200, resp.status)

        return self._exec_with_server(helper)


if __name__ == '__main__':
    unittest.main(verbosity=2)
