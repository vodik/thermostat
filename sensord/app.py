import asyncio
import collections
import json
import math
import random
import sys

from aiohttp import web
from aiohttp_index import IndexMiddleware
from dht22 import Sensor
from dht22.pubsub import Publisher
import msgpack
import zmq
import zmq.asyncio

from . import meteorology


context = zmq.asyncio.Context()


async def read_sensor(sensor):
    identifier, (humidity, temperature) = await sensor.read()
    dewpoint = meteorology.dewpoint(temperature, humidity)
    humidex = meteorology.humidex(temperature, dewpoint)

    sensor, name = identifier.decode().split('/')

    return {'sensor': {'type': sensor,
                       'name': name},
            'humidity': humidity,
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
    reader = context.socket(zmq.PULL)
    reader.bind('tcp://0.0.0.0:6667')

    async def read_loop(publisher):
        while True:
            print('READING')
            identifier, measurement = await reader.recv_multipart()
            print(identifier, measurement)
            assert identifier.startswith(b'dht22')
            payload = msgpack.unpackb(measurement, use_list=False)
            sensor.publish((identifier, payload))

    sensor = Publisher()
    asyncio.ensure_future(read_loop(sensor))
    app['sensor'] = sensor


def app_factory(args=()):
    app = web.Application(middlewares=[IndexMiddleware()])
    app.on_startup.append(start_sensor)

    app.router.add_get('/api/v1/sensor', get_sensor)
    app.router.add_get('/api/v1/sensor/ws', websocket_sensor)
    app.router.add_static('/', 'static')
    return app
