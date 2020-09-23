import argparse
import asyncio

import uvloop
from aiohttp import web

from auth.service import Service

parser = argparse.ArgumentParser(description='LDAP Auth Service')
parser.add_argument('--port')


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    service = Service()
    app = service.app

    args = parser.parse_args()
    web.run_app(app, port=args.port)
