import json

from aiohttp import web
from aiohttp.abc import Request

from auth.jwt_api import JwtApi
from auth.ldap_api import LdapApi


class AuthApi(object):
    __slots__ = ['_jwt', '_ldap']

    def __init__(self):
        self._jwt = JwtApi()
        self._ldap = LdapApi()

    async def login(self, request: Request):
        data = await request.post()
        usr = data.get('user')
        pwd = data.get('password')
        is_valid = self._ldap.validate(usr=usr, pwd=pwd)
        if is_valid:
            token = self._jwt.get_token(usr)
            return web.json_response(status=200, data={'token': token})
        else:
            return web.json_response(
                status=401, data={'message': 'invalid user name or password'})
