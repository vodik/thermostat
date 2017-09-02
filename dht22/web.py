import asyncio
import collections
import json
import math
import random
import sys

from aiohttp import web
from aiohttp_index import IndexMiddleware

from . import meteorology
from .sensor import Sensor


async def read_sensor(sensor):
    humidity, temperature = await sensor.read()
    dewpoint = meteorology.dewpoint(temperature, humidity)
    humidex = meteorology.humidex(temperature, dewpoint)

    return {'humidity': humidity,
            'temperature': temperature,
            'dewpoint': dewpoint,
            'humidex': humidex,
            'message': meteorology.humidex_level(humidex)}


async def get_sensor(request):
    sensor = request.app['sensor']
    return web.json_response(await read_sensor(sensor))


async def websocket_sensor(request):
    subscription = request.app['sensor'].subscribe()
    websocket = web.WebSocketResponse()

    await websocket.prepare(request)
    while True:
        payload = await read_sensor(subscription)
        await websocket.send_str(json.dumps(payload))

    return websocket


async def start_sensor(app):
    sensor = Sensor(4)
    asyncio.ensure_future(sensor.poll())
    app['sensor'] = sensor


def app_factory(args=()):
    """Create a new aiohttp web server.

    Then connect to our Vega so we can drive it and add our routes.
    """
    app = web.Application(middlewares=[IndexMiddleware()])
    app.on_startup.append(start_sensor)

    app.router.add_get('/api/v1/sensor', get_sensor)
    app.router.add_get('/api/v1/sensor/ws', websocket_sensor)
    app.router.add_static('/', 'static')
    return app
